"""S3 service for uploading data and generating presigned URLs."""

import io
import boto3
from botocore.config import Config
from typing import Dict, Any, Union

__all__ = ["upload", "generate_presigned_url"]

def upload(data: Union[bytes, str], object_name: str, mimetype: str, s3_config: Dict[str, Any]) -> None:
    """
    Uploads bytes or a local file to S3.
    
    Args:
        data: The raw bytes to upload, or a string path to a local file.
        object_name: The target S3 object key.
        mimetype: The content type of the file.
        s3_config: Configuration dictionary containing bucket, endpoint_url, access_key, secret_key, region.
    """
    s3_client = _get_client(s3_config)
    bucket = s3_config['bucket']
    
    if isinstance(data, bytes):
        s3_client.upload_fileobj(
            io.BytesIO(data),
            bucket,
            object_name,
            ExtraArgs={'ContentType': mimetype}
        )
    else:
        # Assume it's a file path
        s3_client.upload_file(
            data, 
            bucket, 
            object_name, 
            ExtraArgs={'ContentType': mimetype}
        )

def generate_presigned_url(object_name: str, s3_config: Dict[str, Any]) -> str:
    """
    Generates a presigned URL for an object in S3.
    
    Args:
        object_name: The S3 object key.
        s3_config: Configuration dictionary containing bucket and expires_in.
        
    Returns:
        A presigned URL string.
    """
    s3_client = _get_client(s3_config)
    bucket = s3_config['bucket']
    
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': object_name},
        ExpiresIn=s3_config.get('expires_in', 3600)
    )
    return url

def _get_client(s3_config: Dict[str, Any]):
    """Internal helper to instantiate the boto3 client."""
    endpoint_url = s3_config.get('endpoint_url')
    
    # Use s3v2 signature for GCS, otherwise s3v4
    sig_version = 's3' if endpoint_url and 'googleapis.com' in endpoint_url else 's3v4'
    config_kwargs = {'signature_version': sig_version}
    
    if s3_config.get('path_style'):
        config_kwargs['s3'] = {'addressing_style': 'path'}

    client_kwargs = {
        'service_name': 's3',
        'aws_access_key_id': s3_config.get('access_key'),
        'aws_secret_access_key': s3_config.get('secret_key'),
        'config': Config(**config_kwargs)
    }
    
    if endpoint_url:
        client_kwargs['endpoint_url'] = endpoint_url
        
    if sig_version == 's3v4':
        client_kwargs['region_name'] = s3_config.get('region', 'us-east-1')

    return boto3.client(**client_kwargs)
