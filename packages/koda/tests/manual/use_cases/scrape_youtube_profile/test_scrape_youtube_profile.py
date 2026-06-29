import asyncio
import base64
import os

# Force Koda to run headed before importing any Koda modules
# so the Settings class picks it up during initialization.
os.environ["KODA_HEADLESS"] = "true"

from worldline import structlog
from koda.use_cases.scrape_youtube_profile.schema import ScrapeYoutubeProfileRequest
from koda.use_cases.scrape_youtube_profile.service import scrape_youtube_profile

logger = structlog.get_logger(__name__)

def save_base64_image(base64_string: str, filename: str, output_dir: str = "output") -> str:
    """Decodes a base64 string (with or without data prefix) or downloads a URL and saves it to a file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    # Type guard if base64_string is inadvertently passed as bytes
    if isinstance(base64_string, bytes):
        base64_string = base64_string.decode("utf-8")
    
    if base64_string.startswith("http://") or base64_string.startswith("https://"):
        import requests
        response = requests.get(base64_string)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(response.content)
        return filepath
        
    # Strip data URI prefix if present
    if "," in base64_string:
        base64_string = base64_string.split(",", 1)[1]
        
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(base64_string))
        
    return filepath

async def main():
    logger.info("Testing YouTube Profile Scraper in Headed Mode...")
    
    req = ScrapeYoutubeProfileRequest(
        url="https://www.youtube.com/@mkbhd",
        formats=["screenshot"],
        timeout=120000,
        maxConcurrency=2
    )

    logger.info("Starting crawler...")
    response = await scrape_youtube_profile(req)

    if not response.success:
        print(f"Failed: {response.error}")
        return

    logger.info("Success! Saving screenshots to tests/manual/output/ ...")
    
    if response.data:
        from koda.utils.file.main import File
        import uuid
        for tab_data in response.data:
            if "screenshot" in tab_data and isinstance(tab_data["screenshot"], File):
                f = tab_data["screenshot"]
                # Use the original filename provided by the File object, fallback to uuid
                save_name = getattr(f, "filename", None) or f"{uuid.uuid4().hex}.png"
                filepath = save_base64_image(
                    base64_string=f.presigned_url or f.base64,
                    filename=save_name,
                    output_dir=os.path.join(os.path.dirname(__file__), "output")
                )
                f.cleanup()
                logger.info(f"Saved: {filepath}")

if __name__ == "__main__":
    asyncio.run(main())
