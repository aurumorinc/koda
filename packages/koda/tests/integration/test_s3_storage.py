import os
import pytest
import aioboto3

from koda.modules.session.repositories.storage.s3 import upload_profile, download_profile
from koda.config.main import settings

# Skip if live S3 credentials are not provided
pytestmark = pytest.mark.skipif(
    not os.getenv("TEST_S3_ENDPOINT_URL") or not os.getenv("TEST_S3_BUCKET_NAME"),
    reason="Live S3 credentials not provided"
)

@pytest.fixture(autouse=True)
def setup_s3_settings():
    """Override settings with test environment variables."""
    original_endpoint = settings.s3_endpoint_url
    original_bucket = settings.s3_bucket_name
    original_access_key = settings.s3_access_key_id
    original_secret_key = settings.s3_secret_access_key
    
    settings.s3_endpoint_url = os.getenv("TEST_S3_ENDPOINT_URL")
    settings.s3_bucket_name = os.getenv("TEST_S3_BUCKET_NAME")
    settings.s3_access_key_id = os.getenv("TEST_S3_ACCESS_KEY_ID")
    settings.s3_secret_access_key = os.getenv("TEST_S3_SECRET_ACCESS_KEY")
    
    yield
    
    settings.s3_endpoint_url = original_endpoint
    settings.s3_bucket_name = original_bucket
    settings.s3_access_key_id = original_access_key
    settings.s3_secret_access_key = original_secret_key

@pytest.fixture
def dummy_profile_dir(tmp_path):
    """Create a dummy profile directory with some files."""
    profile_dir = tmp_path / "dummy_profile"
    profile_dir.mkdir()
    
    (profile_dir / "file1.txt").write_text("hello world")
    (profile_dir / "file2.json").write_text('{"key": "value"}')
    
    sub_dir = profile_dir / "subdir"
    sub_dir.mkdir()
    (sub_dir / "file3.txt").write_text("nested content")
    
    return str(profile_dir)

@pytest.mark.asyncio
async def test_s3_upload_download_flow(dummy_profile_dir, tmp_path):
    session_id = "test_session_123"
    
    # 1. Upload
    s3_key = await upload_profile(dummy_profile_dir, session_id)
    assert s3_key == f"profiles/{session_id}.zip"
    
    # 2. Download to a new directory
    extract_dir = str(tmp_path / "extracted_profile")
    await download_profile(s3_key, extract_dir)
    
    # 3. Verify contents
    assert os.path.exists(os.path.join(extract_dir, "file1.txt"))
    assert os.path.exists(os.path.join(extract_dir, "file2.json"))
    assert os.path.exists(os.path.join(extract_dir, "subdir", "file3.txt"))
    
    with open(os.path.join(extract_dir, "file1.txt"), "r") as f:
        assert f.read() == "hello world"
        
    # 4. Overwrite (Upload modified profile)
    with open(os.path.join(dummy_profile_dir, "file1.txt"), "w") as f:
        f.write("modified content")
        
    await upload_profile(dummy_profile_dir, session_id)
    
    # 5. Download again and verify overwrite
    extract_dir_2 = str(tmp_path / "extracted_profile_2")
    await download_profile(s3_key, extract_dir_2)
    
    with open(os.path.join(extract_dir_2, "file1.txt"), "r") as f:
        assert f.read() == "modified content"
        
    # 6. Cleanup S3
    session = aioboto3.Session()
    kwargs = {
        "region_name": settings.s3_region_name,
        "endpoint_url": settings.s3_endpoint_url,
        "aws_access_key_id": settings.s3_access_key_id,
        "aws_secret_access_key": settings.s3_secret_access_key,
    }
    async with session.client('s3', **kwargs) as s3:
        await s3.delete_object(Bucket=settings.s3_bucket_name, Key=s3_key)
