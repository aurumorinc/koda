import asyncio
import base64
import inspect
import os

# Force Koda to run headed before importing any Koda modules
# so the Settings class picks it up during initialization.
os.environ["KODA_HEADLESS"] = "true"

import structlog
from koda.use_cases.scrape_youtube_profile.schema import ScrapeYoutubeProfileRequest
from koda.use_cases.scrape_youtube_profile.service import scrape_youtube_profile

logger = structlog.get_logger(__name__)

def save_base64_image(base64_string: str, filename: str, output_dir: str = "output") -> str:
    """Decodes a base64 string (with or without data prefix) or downloads a URL and saves it to a file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    if isinstance(base64_string, bytes):
        base64_string = base64_string.decode("utf-8")
    
    if base64_string.startswith("http://") or base64_string.startswith("https://"):
        import requests
        response = requests.get(base64_string)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(response.content)
        return filepath
        
    if "," in base64_string:
        base64_string = base64_string.split(",", 1)[1]
        
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(base64_string))
        
    return filepath

async def main():
    req = ScrapeYoutubeProfileRequest(
        url="https://www.youtube.com/@LinusTechTips",
        formats=["screenshot"],
        timeout=300000,
        maxConcurrency=1
    )

    logger.info("Starting crawler...")
    response = await scrape_youtube_profile(req)

    if not response.success:
        print(f"Failed: {response.error}")
        return

    logger.info("Success! Saving screenshots to tests/manual/output/ ...")
    
    if response.data:
        from oort.file.main import File
        import uuid
        for tab_data in response.data:
            if "screenshot" in tab_data and isinstance(tab_data["screenshot"], File):
                f = tab_data["screenshot"]
                save_name = getattr(f, "filename", None) or f"{uuid.uuid4().hex}.png"
                
                presigned = f.presigned_url
                if inspect.isawaitable(presigned):
                    presigned = await presigned
                
                b64_val = presigned or f.base64
                filepath = save_base64_image(
                    base64_string=b64_val,
                    filename=save_name,
                    output_dir=os.path.join(os.path.dirname(__file__), "output")
                )
                f.cleanup()
                logger.info(f"Saved: {filepath}")

if __name__ == "__main__":
    asyncio.run(main())
