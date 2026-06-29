import os
import tempfile
import base64
import pytest
from unittest.mock import patch, MagicMock

from koda.utils.file import File

@pytest.fixture
def mock_s3_upload():
    with patch("koda.utils.file.main.upload") as mock:
        yield mock

@pytest.fixture
def mock_s3_presigned():
    with patch("koda.utils.file.main.generate_presigned_url") as mock:
        mock.return_value = "https://s3.amazonaws.com/test-bucket/file.png"
        yield mock

@pytest.fixture
def mock_settings():
    with patch("koda.utils.file.main.settings") as mock_settings:
        mock_settings.s3.bucket_name = "test-bucket"
        yield mock_settings

class TestFile:
    
    def test_from_bytes(self):
        data = b"test bytes"
        with File.from_bytes(data, "test.txt", "text/plain") as f:
            assert os.path.exists(f.path)
            assert f.filename == "test.txt"
            assert f.mimetype == "text/plain"
            assert f.bytes == data
        
        assert not os.path.exists(f.path)
        assert f._is_cleaned_up

    def test_from_base64(self):
        data = b"test bytes"
        b64_str = base64.b64encode(data).decode("utf-8")
        
        # Without data URI prefix
        with File.from_base64(b64_str, "test.txt", "text/plain") as f:
            assert f.bytes == data
            assert f.base64 == f"data:text/plain;base64,{b64_str}"
            
        # With data URI prefix
        data_uri = f"data:text/plain;base64,{b64_str}"
        with File.from_base64(data_uri, "test2.txt", "text/plain") as f:
            assert f.bytes == data

    def test_from_path(self):
        fd, temp_path = tempfile.mkstemp()
        os.close(fd)
        with open(temp_path, "wb") as f:
            f.write(b"test path")
            
        try:
            with File.from_path(temp_path, "original.txt") as kf:
                assert kf.bytes == b"test path"
                assert kf.path != temp_path
                assert os.path.exists(kf.path)
            
            assert not os.path.exists(kf.path)
            assert os.path.exists(temp_path)
        finally:
            os.remove(temp_path)

    @patch("requests.get")
    def test_from_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"chunk1", b"chunk2"]
        mock_get.return_value = mock_response
        
        with File.from_url("http://example.com/file.png") as f:
            assert f.filename == "file.png"
            assert f.bytes == b"chunk1chunk2"
            assert f.url == "http://example.com/file.png"

    @pytest.mark.asyncio
    async def test_from_playwright_download(self):
        mock_download = MagicMock()
        mock_download.suggested_filename = "downloaded.txt"
        
        async def mock_save_as(path):
            with open(path, "wb") as f:
                f.write(b"downloaded content")
        
        mock_download.save_as = mock_save_as
        
        f = await File.from_playwright_download(mock_download)
        assert f.filename == "downloaded.txt"
        assert f.bytes == b"downloaded content"
        f.cleanup()

    def test_to_playwright_input(self):
        data = b"input"
        with File.from_bytes(data, "input.txt", "text/plain") as f:
            playwright_input = f.to_playwright_input()
            assert playwright_input["name"] == "input.txt"
            assert playwright_input["mimeType"] == "text/plain"
            assert playwright_input["buffer"] == data

    def test_presigned_url(self, mock_s3_upload, mock_s3_presigned, mock_settings):
        data = b"s3 test"
        with File.from_bytes(data, "s3.txt", "text/plain") as f:
            url1 = f.presigned_url
            assert url1 == "https://s3.amazonaws.com/test-bucket/file.png"
            mock_s3_upload.assert_called_once()
            mock_s3_presigned.assert_called_once()
            
            # Second call should use cache
            url2 = f.presigned_url
            assert url2 == "https://s3.amazonaws.com/test-bucket/file.png"
            mock_s3_upload.assert_called_once()
            mock_s3_presigned.assert_called_once()