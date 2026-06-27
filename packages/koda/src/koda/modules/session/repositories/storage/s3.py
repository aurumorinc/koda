import os
import shutil
import aioboto3
from typing import Optional

from koda.config.main import settings
from worldline import structlog

logger = structlog.get_logger(__name__)

def _get_s3_client_kwargs() -> dict:
    """Helper to build aioboto3 client kwargs from settings."""
    from botocore.config import Config
    
    endpoint_url = settings.s3_endpoint_url
    
    # Use s3v2 signature for GCS, otherwise s3v4
    sig_version = 's3' if endpoint_url and 'googleapis.com' in endpoint_url else 's3v4'
    config_kwargs = {'signature_version': sig_version}
    
    if settings.s3_addressing_style != "auto":
        config_kwargs['s3'] = {'addressing_style': settings.s3_addressing_style}
        
    kwargs = {
        "service_name": "s3",
        "config": Config(**config_kwargs)
    }
    
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url
        
    if settings.s3_access_key_id:
        kwargs["aws_access_key_id"] = settings.s3_access_key_id
    if settings.s3_secret_access_key:
        kwargs["aws_secret_access_key"] = settings.s3_secret_access_key
        
    if sig_version == 's3v4':
        kwargs["region_name"] = settings.s3_region_name
        
    return kwargs

async def download_profile(s3_key: str, local_extract_dir: str) -> None:
    """
    Downloads a zipped profile from S3 and extracts it to local_extract_dir.
    """
    if not settings.s3_bucket_name:
        raise ValueError("S3_BUCKET_NAME is not configured.")

    zip_path = f"{local_extract_dir}.zip"
    
    session = aioboto3.Session()
    async with session.client(**_get_s3_client_kwargs()) as s3:
        logger.info("Downloading profile from S3", extra={"s3_key": s3_key, "bucket": settings.s3_bucket_name})
        try:
            await s3.download_file(settings.s3_bucket_name, s3_key, zip_path)
        except Exception as e:
            logger.error("Failed to download profile from S3", exc_info=True, extra={"s3_key": s3_key})
            raise e

    logger.debug("Extracting profile", extra={"zip_path": zip_path, "extract_dir": local_extract_dir})
    shutil.unpack_archive(zip_path, local_extract_dir)
    
    # Clean up the downloaded zip file
    if os.path.exists(zip_path):
        os.remove(zip_path)

async def upload_profile(local_dir: str, session_id: str) -> str:
    """
    Compresses local_dir into a zip, uploads it to S3, and returns the s3_key.
    """
    if not settings.s3_bucket_name:
        raise ValueError("S3_BUCKET_NAME is not configured.")

    s3_key = f"profiles/{session_id}.zip"
    zip_path = f"{local_dir}.zip"
    
    logger.debug("Compressing profile", extra={"local_dir": local_dir, "zip_path": zip_path})
    # shutil.make_archive adds the .zip extension automatically, so we pass the base name
    shutil.make_archive(local_dir, 'zip', local_dir)
    
    session = aioboto3.Session()
    async with session.client(**_get_s3_client_kwargs()) as s3:
        logger.info("Uploading profile to S3", extra={"s3_key": s3_key, "bucket": settings.s3_bucket_name})
        try:
            await s3.upload_file(zip_path, settings.s3_bucket_name, s3_key)
        except Exception as e:
            logger.error("Failed to upload profile to S3", exc_info=True, extra={"s3_key": s3_key})
            raise e
        finally:
            # Clean up the created zip file
            if os.path.exists(zip_path):
                os.remove(zip_path)
                
    return s3_key
