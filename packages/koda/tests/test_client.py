"""Integration tests for KodaClient."""

import pytest
import asyncio
from pathlib import Path
import tempfile

from unittest.mock import patch

from koda.client import KodaClient
from koda.config import ScrapeOptions, Action, KodaError, WebhookConfig

@pytest.fixture
def dummy_html_file():
    """Create a temporary HTML file for testing."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dummy Page</title>
        <meta name="description" content="Test description">
    </head>
    <body>
        <main>
            <h1>Test Content</h1>
            <p>This is a paragraph.</p>
        </main>
        <footer><p>Footer stuff</p></footer>
    </body>
    </html>
    """
    fd, path = tempfile.mkstemp(suffix=".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
        
    yield Path(path)
    
    Path(path).unlink()


@pytest.mark.asyncio
@patch("koda.services.scrape.FileService.upload_and_presign")
async def test_kodaclient_scrape_local_file(mock_upload, dummy_html_file):
    """Test scraping a local HTML file."""
    mock_upload.return_value = "https://mock-s3-url.com/image.jpg"
    
    async with KodaClient() as client:
        response = await client.scrape(
            dummy_html_file, 
            formats=["markdown", "metadata", "screenshot"],
            only_main_content=True,
            s3_config={"bucket": "test"}
        )
        
        assert response.error is None
        assert response.metadata is not None
        assert response.metadata.get("title") == "Dummy Page"
        assert response.metadata.get("description") == "Test description"
        
        assert response.markdown is not None
        assert "Test Content" in response.markdown
        assert "This is a paragraph" in response.markdown
        assert "Footer stuff" not in response.markdown
        
        assert response.screenshot == "https://mock-s3-url.com/image.jpg"
        mock_upload.assert_called_once()


@pytest.mark.asyncio
async def test_kodaclient_unstarted_raises_error():
    """Test that using client without starting raises an error."""
    client = KodaClient()
    with pytest.raises(KodaError):
        await client.scrape("http://example.com")

@pytest.mark.asyncio
@patch("koda.services.scrape.FileService.upload_and_presign")
@patch("urllib.request.urlopen")
async def test_kodaclient_with_webhook(mock_urlopen, mock_upload, dummy_html_file):
    """Test scraping with a webhook callback."""
    mock_upload.return_value = "https://mock-s3-url.com/image.jpg"
    
    webhook_cfg = WebhookConfig(
        url="http://test-webhook.com/callback",
        metadata={"user_id": 123}
    )
    
    async with KodaClient() as client:
        response = await client.scrape(
            dummy_html_file, 
            formats=["markdown"],
            webhook=webhook_cfg
        )
        
        assert response.error is None
        mock_urlopen.assert_called_once()
        
        # Verify the webhook request
        request = mock_urlopen.call_args[0][0]
        assert request.full_url == "http://test-webhook.com/callback"
        
        import json
        payload = json.loads(request.data.decode("utf-8"))
        assert payload["success"] is True
        assert "data" in payload
        assert "markdown" in payload["data"]
        assert payload["user_id"] == 123
