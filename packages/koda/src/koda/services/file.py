"""S3 service for uploading files and generating presigned URLs."""

import boto3
from botocore.config import Config
from typing import Dict, Any

__all__ = ["FileService"]

class FileService:
    """Service responsible for S3 operations."""

    @classmethod
    def upload_and_presign(cls, file_path: str, object_name: str, mimetype: str, s3_config: Dict[str, Any]) -> str:
        """
        Uploads a file to S3 and returns a presigned URL.
        
        Args:
            file_path: Path to the local file.
            object_name: The target S3 object key.
            mimetype: The content type of the file.
            s3_config: Configuration dictionary containing bucket, endpoint_url, access_key, secret_key, region, expires_in.
            
        Returns:
            A presigned URL string for the uploaded object.
        """
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

        s3_client = boto3.client(**client_kwargs)
        bucket = s3_config['bucket']
        
        # Upload
        s3_client.upload_file(
            file_path, 
            bucket, 
            object_name, 
            ExtraArgs={'ContentType': mimetype}
        )
        
        # Presign
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': object_name},
            ExpiresIn=s3_config.get('expires_in', 3600)
        )
        return url
