import os
import uuid
import tempfile
import shutil
import mimetypes
import base64
import requests
from typing import Optional
from worldline import structlog

from koda.config.main import settings
from koda.utils.file.service import upload, generate_presigned_url

logger = structlog.get_logger(__name__)

class File:
    """
    A wrapper around a local temporary file, with a mandatory filename and mimetype.
    Supports lazy uploading to S3 to generate a presigned URL.
    """
    def __init__(self, path: str, filename: str, mimetype: str, url: Optional[str] = None):
        self.path = path
        self.filename = filename
        self.mimetype = mimetype
        self.url = url
        self._presigned_url: Optional[str] = None
        self._is_cleaned_up = False
        self._object_name: Optional[str] = None
        self._buffer: Optional[bytes] = None

    def __enter__(self) -> "File":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.cleanup()

    def cleanup(self) -> None:
        """Deletes the underlying temporary file."""
        if not self._is_cleaned_up and os.path.exists(self.path):
            try:
                os.remove(self.path)
                self._is_cleaned_up = True
                logger.debug("Cleaned up temporary file: %s", self.path)
            except OSError as e:
                logger.warning("Failed to clean up temporary file %s: %s", self.path, e)

    @property
    def bytes(self) -> bytes:
        """Lazily reads the file into memory."""
        if self._buffer is None:
            with open(self.path, "rb") as f:
                self._buffer = f.read()
        return self._buffer

    @property
    def base64(self) -> str:
        """Lazily generates a base64 data URI from the buffer."""
        b64_str = base64.b64encode(self.bytes).decode("utf-8")
        return f"data:{self.mimetype};base64,{b64_str}"

    @property
    def presigned_url(self) -> Optional[str]:
        """Lazily uploads the file to S3 and returns the presigned URL."""
        if self._presigned_url:
            return self._presigned_url
            
        if not settings.s3 or not settings.s3.bucket_name:
            logger.warning("S3 is not configured. Cannot generate presigned URL.")
            return None
        
        # Ensure a unique object name in S3 to prevent collisions
        self._object_name = f"{uuid.uuid4().hex}_{self.filename}"
        logger.info("Uploading %s to S3 as %s...", self.path, self._object_name)
        
        # Utilize Koda's existing upload service (passing the local file path)
        upload(self.path, self._object_name, self.mimetype)
        
        # Utilize Koda's existing presign service
        self._presigned_url = generate_presigned_url(self._object_name)
        return self._presigned_url

    def to_playwright_input(self) -> dict:
        """Returns the dictionary format required by Playwright's set_input_files."""
        return {
            "name": self.filename,
            "mimeType": self.mimetype,
            "buffer": self.bytes
        }

    @classmethod
    def _get_temp_path(cls, filename: str) -> str:
        """Returns a temporary path for the file."""
        ext = os.path.splitext(filename)[1]
        fd, path = tempfile.mkstemp(suffix=ext)
        os.close(fd)
        return path

    @classmethod
    def create_empty(cls, filename: str, mimetype: Optional[str] = None, touch: bool = False) -> "File":
        if not mimetype:
            mimetype, _ = mimetypes.guess_type(filename)
            mimetype = mimetype or "application/octet-stream"
            
        path = cls._get_temp_path(filename)
        if touch:
            open(path, 'a').close()
        return cls(path, filename, mimetype)

    @classmethod
    def from_bytes(cls, data: bytes, filename: str, mimetype: Optional[str] = None) -> "File":
        """Ideal for Playwright, Crawlee, and Stagehand (`page.screenshot()`)."""
        if not mimetype:
            mimetype, _ = mimetypes.guess_type(filename)
            mimetype = mimetype or "application/octet-stream"
            
        path = cls._get_temp_path(filename)
        with open(path, 'wb') as f:
            if isinstance(data, str):
                f.write(data.encode("utf-8"))
            else:
                f.write(data)
        return cls(path, filename, mimetype)

    @classmethod
    def from_base64(cls, base64_string: str, filename: str, mimetype: Optional[str] = None) -> "File":
        """Ideal for Crawl4AI (`result.screenshot`)."""
        if isinstance(base64_string, bytes):
            base64_string = base64_string.decode("utf-8")
            
        if "," in base64_string:
            base64_string = base64_string.split(",", 1)[1]
            
        data = base64.b64decode(base64_string)
        return cls.from_bytes(data, filename, mimetype)

    @classmethod
    def from_url(cls, url: str, filename: Optional[str] = None, mimetype: Optional[str] = None) -> "File":
        """Ideal for capturing remote assets seamlessly."""
        if not filename:
            filename = os.path.basename(url.split("?")[0]) or f"{uuid.uuid4().hex}.tmp"
            
        if not mimetype:
            mimetype, _ = mimetypes.guess_type(filename)
            mimetype = mimetype or "application/octet-stream"
            
        path = cls._get_temp_path(filename)
        logger.info("Downloading %s to %s...", url, path)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        return cls(path, filename, mimetype, url=url)

    @classmethod
    def from_path(cls, source_path: str, filename: Optional[str] = None) -> "File":
        """Ideal for wrapping existing disk files."""
        if not filename:
            filename = os.path.basename(source_path)
            
        mimetype, _ = mimetypes.guess_type(filename)
        mimetype = mimetype or "application/octet-stream"
        
        path = cls._get_temp_path(filename)
        shutil.copy2(source_path, path)
        return cls(path, filename, mimetype)

    @classmethod
    async def from_playwright_download(cls, download: any, filename: Optional[str] = None) -> "File":
        """Awaits playwright download and wraps the resulting file."""
        if not filename:
            filename = download.suggested_filename
        
        mimetype, _ = mimetypes.guess_type(filename)
        mimetype = mimetype or "application/octet-stream"
        
        path = cls._get_temp_path(filename)
        await download.save_as(path)
        return cls(path, filename, mimetype)
