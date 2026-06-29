import asyncio
import base64
import os

# Force Koda to run headed before importing any Koda modules
# so the Settings class picks it up during initialization.
os.environ.setdefault("KODA_HEADLESS", "false")

from worldline import structlog
from koda.use_cases.scrape_youtube_profile.schema import ScrapeYoutubeProfileRequest
from koda.use_cases.scrape_youtube_profile.service import scrape_youtube_profile

logger = structlog.get_logger(__name__)

def save_base64_image(b64_string: str, filename: str, output_dir: str = "output") -> str:
    """Decodes a base64 string (with or without data prefix) and saves it to a file."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Strip data URI prefix if present
    if "," in b64_string:
        b64_string = b64_string.split(",", 1)[1]
        
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(b64_string))
        
    return filepath

async def main():
    logger.info("Testing YouTube Profile Scraper in Headed Mode...")
    
    req = ScrapeYoutubeProfileRequest(
        url="https://www.youtube.com/@mkbhd",
        tabs=["home", "videos"],
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
    
    for tab_data in response.data:
        tab_name = tab_data["tab_name"]
        if "screenshot" in tab_data:
            filepath = save_base64_image(
                b64_string=tab_data["screenshot"], 
                filename=f"youtube_{tab_name.lower()}.png",
                output_dir=os.path.join(os.path.dirname(__file__), "output")
            )
            logger.info(f"Saved: {filepath}")

if __name__ == "__main__":
    asyncio.run(main())
