"""S3 service for uploading data and generating presigned URLs."""

import io
import boto3
from botocore.config import Config
from boto3.s3.transfer import TransferConfig
from typing import Dict, Any, Union
from koda.config.main import settings

__all__ = ["upload", "generate_presigned_url"]

def upload(data: Union[bytes, str], object_name: str, mimetype: str) -> None:
    """
    Uploads bytes or a local file to S3.
    
    Args:
        data: The raw bytes to upload, or a string path to a local file.
        object_name: The target S3 object key.
        mimetype: The content type of the file.
    """
    s3_client = _get_client()
    bucket = settings.s3.bucket_name
    
    # Disable multipart upload up to 500MB to avoid SignatureDoesNotMatch errors with S3-compatible providers
    transfer_config = TransferConfig(multipart_threshold=500 * 1024 * 1024)
    
    if isinstance(data, bytes):
        s3_client.upload_fileobj(
            io.BytesIO(data),
            bucket,
            object_name,
            ExtraArgs={'ContentType': mimetype},
            Config=transfer_config
        )
    else:
        # Assume it's a file path
        s3_client.upload_file(
            data,
            bucket,
            object_name,
            ExtraArgs={'ContentType': mimetype},
            Config=transfer_config
        )

def generate_presigned_url(object_name: str, expires_in: int = 3600) -> str:
    """
    Generates a presigned URL for an object in S3.
    
    Args:
        object_name: The S3 object key.
        expires_in: Expiration time for presigned URLs in seconds.
        
    Returns:
        A presigned URL string.
    """
    s3_client = _get_client()
    bucket = settings.s3.bucket_name
    
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': object_name},
        ExpiresIn=expires_in
    )
    return url

def _get_client():
    """Internal helper to instantiate the boto3 client."""
    if not settings.s3:
        raise ValueError("S3 configuration is missing.")
        
    endpoint_url = settings.s3.endpoint_url
    
    # Use s3v2 signature for GCS, otherwise s3v4
    sig_version = 's3' if endpoint_url and 'googleapis.com' in endpoint_url else 's3v4'
    config_kwargs: Dict[str, Any] = {'signature_version': sig_version}
    
    if settings.s3.addressing_style == "path":
        config_kwargs['s3'] = {'addressing_style': 'path'}

    client_kwargs: Dict[str, Any] = {
        'aws_access_key_id': settings.s3.access_key_id,
        'aws_secret_access_key': settings.s3.secret_access_key,
        'config': Config(**config_kwargs)
    }
    
    if endpoint_url:
        client_kwargs['endpoint_url'] = endpoint_url
        
    if sig_version == 's3v4':
        client_kwargs['region_name'] = settings.s3.region_name

    return boto3.client('s3', **client_kwargs)
