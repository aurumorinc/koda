"""Integration tests for KodaClient."""

import pytest
import asyncio
from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock

from koda.client import KodaClient
from koda.schemas.page import ScrapeRequest, Action
from koda.schemas.webhook import WebhookConfig
from koda.exceptions import KodaError

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
@patch("koda.client.file.upload")
@patch("koda.client.file.generate_presigned_url")
async def test_kodaclient_scrape_local_file(mock_presign, mock_upload, dummy_html_file):
    """Test scraping a local HTML file."""
    mock_presign.return_value = "https://mock-s3-url.com/image.jpg"
    
    async with KodaClient() as client:
        request = ScrapeRequest(
            url=str(dummy_html_file),
            formats=["markdown", "metadata", "screenshot"],
            only_main_content=True,
            s3_config={"bucket": "test"}
        )
        response = await client.scrape(request)
        
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
        await client.scrape(ScrapeRequest(url="http://example.com"))

@pytest.mark.asyncio
@patch("koda.client.file.upload")
@patch("koda.client.webhook.handle")
async def test_kodaclient_with_webhook(mock_webhook_handle, mock_upload, dummy_html_file):
    """Test scraping with a webhook callback."""
    webhook_cfg = WebhookConfig(
        url="http://test-webhook.com/callback",
        metadata={"user_id": 123}
    )
    
    async with KodaClient() as client:
        request = ScrapeRequest(
            url=str(dummy_html_file),
            formats=["markdown"],
            webhook=webhook_cfg
        )
        response = await client.scrape(request)
        
        assert response.error is None
        mock_webhook_handle.assert_called_once()
        
        # Verify the webhook handle call
        args = mock_webhook_handle.call_args[0]
        assert args[0].url == "http://test-webhook.com/callback"
        assert args[1].url == str(dummy_html_file)
