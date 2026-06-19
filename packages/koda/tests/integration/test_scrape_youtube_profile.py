import pytest
from unittest.mock import AsyncMock, patch, MagicMock

import sys
import os
import importlib.util
from unittest.mock import MagicMock

# Mock wmill before loading
class MockWmill:
    @staticmethod
    def get_resource(res):
        return None

sys.modules["wmill"] = MagicMock()
sys.modules["wmill"].get_resource = MockWmill.get_resource

# We need to load the module dynamically because of the hyphen in koda-api
script_path = os.path.join(os.path.dirname(__file__), "../../../../apps/koda-api/f/koda/scouts/scrape_youtube_profile.py")
spec = importlib.util.spec_from_file_location("scrape_youtube_profile", script_path)
yp = importlib.util.module_from_spec(spec)
sys.modules["scrape_youtube_profile"] = yp
spec.loader.exec_module(yp)

_run_youtube_scrape = yp._run_youtube_scrape

@pytest.mark.asyncio
@patch("scrape_youtube_profile.KodaClient")
async def test_youtube_orchestrator_success(mock_client_class):
    mock_client = AsyncMock()
    
    # First scrape for resolution
    res_initial = MagicMock()
    res_initial.error = None
    res_initial.metadata = {
        "og:url": "https://www.youtube.com/@youtube"
    }
    
    # Second scrape (batch)
    res_home = MagicMock(url="https://www.youtube.com/@youtube", success=True, markdown="Home Page Markdown", error=None)
    res_home.html = "<html>Home</html>"
    res_home.links = {"link1": "test1"}
    res_home.screenshot = "http://s3/home.jpg"
    
    res_about = MagicMock(url="https://www.youtube.com/@youtube?about=1", success=True, markdown="About Markdown", error=None)
    res_about.html = "<html>About</html>"
    res_about.links = {"link_about": "test_about"}
    res_about.screenshot = "http://s3/about.jpg"
    
    res_videos = MagicMock(url="https://www.youtube.com/@youtube/videos", success=True, markdown="Videos Markdown", error=None)
    res_videos.html = "<html>Videos</html>"
    res_videos.links = {"link2": "test2"}
    res_videos.screenshot = "http://s3/videos.jpg"
    
    batch_res = MagicMock()
    batch_res.success = True
    batch_res.results = [res_home, res_about, res_videos]

    mock_client.scrape.return_value = res_initial
    mock_client.batch_scrape.return_value = batch_res
    
    mock_client_class.return_value.__aenter__.return_value = mock_client

    result = await _run_youtube_scrape(
        url="https://www.youtube.com/@youtube",
        formats=["markdown", "links", "screenshot"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource=None,
        webhook=None,
        scroll_limit=1,
        tabs=["videos"]
    )
    
    assert result["success"] is True
    assert "data" in result
    assert "markdown" in result["data"]
    assert "links" in result["data"]
    assert "screenshots" in result["data"]
    
    assert "Home Page Markdown" in result["data"]["markdown"]
    assert "Videos Markdown" in result["data"]["markdown"]
    assert "About Markdown" in result["data"]["markdown"]
    
    assert "Home" in result["data"]["links"]
    assert "Videos" in result["data"]["links"]
    assert "About" in result["data"]["links"]
    
    assert result["data"]["screenshots"]["Home"] == "http://s3/home.jpg"
    assert result["data"]["screenshots"]["About"] == "http://s3/about.jpg"

@pytest.mark.asyncio
@patch("scrape_youtube_profile.KodaClient")
async def test_youtube_orchestrator_redirect(mock_client_class):
    mock_client = AsyncMock()
    
    # First scrape for resolution (from a redirect URL)
    res_initial = MagicMock()
    res_initial.error = None
    res_initial.metadata = {
        "og:url": "https://www.youtube.com/@mkbhd/featured"
    }
    
    batch_res = MagicMock()
    batch_res.success = True
    batch_res.results = [
        MagicMock(url="https://www.youtube.com/@mkbhd", success=True, markdown="Home Markdown", error=None, html=None, links=None, screenshot=None)
    ]
    
    mock_client.scrape.return_value = res_initial
    mock_client.batch_scrape.return_value = batch_res
    
    mock_client_class.return_value.__aenter__.return_value = mock_client

    result = await _run_youtube_scrape(
        url="https://crm.link/123",
        formats=["markdown"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource=None,
        webhook=None,
        scroll_limit=1,
        tabs=[]
    )
    
    assert result["success"] is True
    
    # Ensure client was called with the stripped base profile url for the batch scrape
    calls = mock_client.batch_scrape.call_args_list
    assert len(calls) == 1
    batch_req = calls[0][0][0]
    
    assert batch_req.requests is not None
    assert len(batch_req.requests) == 2  # Home + About (no sub tabs passed in this test)
    assert batch_req.requests[0].url == "https://www.youtube.com/@mkbhd"
    assert batch_req.requests[1].url == "https://www.youtube.com/@mkbhd?about=1"

@pytest.mark.asyncio
@patch("scrape_youtube_profile.KodaClient")
async def test_youtube_orchestrator_invalid_handle(mock_client_class):
    mock_client = AsyncMock()
    
    # First scrape for resolution
    res_initial = MagicMock()
    res_initial.error = None
    res_initial.metadata = {
        "url": "https://www.youtube.com/404"
    }
    
    batch_res = MagicMock()
    batch_res.success = True
    # In batch, error is stored inside the individual ScrapeResponse
    batch_res.results = [
        MagicMock(url="https://www.youtube.com/404", success=False, error="404 Not Found", markdown=None, html=None, links=None, screenshot=None)
    ]
    
    mock_client.scrape.return_value = res_initial
    mock_client.batch_scrape.return_value = batch_res
    
    mock_client_class.return_value.__aenter__.return_value = mock_client

    result = await _run_youtube_scrape(
        url="https://youtube.com/404",
        formats=["markdown"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource=None,
        webhook=None,
        scroll_limit=1,
        tabs=[]
    )
    
    # It still returns success=True from the orchestrator perspective, 
    # but the markdown will contain the error message for that tab.
    assert result["success"] is True
    assert "Error: 404 Not Found" in result["data"]["markdown"]
