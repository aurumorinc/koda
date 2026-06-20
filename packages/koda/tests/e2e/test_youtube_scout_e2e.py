import pytest
import asyncio
from typing import Dict, Any

import sys
import os
import importlib.util
from unittest.mock import MagicMock

class MockWmill:
    @staticmethod
    def get_resource(res):
        return None

sys.modules["wmill"] = MagicMock()
sys.modules["wmill"].get_resource = MockWmill.get_resource

script_path = os.path.join(os.path.dirname(__file__), "../../../../apps/koda-api/f/koda/scouts/scrape_youtube_profile.py")
spec = importlib.util.spec_from_file_location("scrape_youtube_profile", script_path)
yp = importlib.util.module_from_spec(spec)
sys.modules["scrape_youtube_profile"] = yp
spec.loader.exec_module(yp)

@pytest.mark.asyncio
async def test_youtube_scout_e2e():
    """
    E2E test verifying the YouTube scout script properly builds the heterogeneous
    batch requests and extracts distinct info for the tabs vs the popup.
    """
    res = await yp._run_youtube_scrape(
        url="https://www.youtube.com/@LinusTechTips",
        formats=["markdown", "html", "screenshot"],
        onlyMainContent=False,
        actions=[],
        timeout=180000, # 3 minutes max
        s3_resource=None,
        webhook=None,
        tabs=["videos", "shorts"],
        scroll_limit=1
    )
    
    assert res.get("success") is True, f"Scrape failed: {res.get('error')}"
    data = res.get("data", {})
    
    # Verify markdown was aggregated
    assert "markdown" in data
    md = data["markdown"]
    print(f"Aggregated markdown length: {len(md)}")
    print(f"Screenshots keys: {data.get('screenshots', {}).keys()}")
    
    assert "Linus Tech Tips" in md
    
    # Verify screenshots dictionary was populated distinctively
    assert "screenshots" in data
    screenshots = data["screenshots"]
    
    # We requested 2 tabs + Home + About = 4 screenshots expected
    assert "Home" in screenshots
    assert "About" in screenshots
    assert "Videos" in screenshots
    assert "Shorts" in screenshots
    
    # Screenshots should be valid data URIs or URLs
    assert screenshots["About"].startswith("data:image/") or screenshots["About"].startswith("http")

