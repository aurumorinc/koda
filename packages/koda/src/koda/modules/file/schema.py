from typing import TypedDict, Optional

class S3Config(TypedDict, total=False):
    """Configuration for S3-compatible storage.
    
    Attributes:
        bucket: The name of the S3 bucket.
        access_key: AWS access key ID.
        secret_key: AWS secret access key.
        endpoint_url: Optional custom endpoint URL (e.g., for MinIO or GCS).
        region: Optional AWS region.
        expires_in: Optional expiration time for presigned URLs in seconds.
        path_style: Optional boolean to use path-style addressing.
    """
    bucket: str
    access_key: str
    secret_key: str
    endpoint_url: Optional[str]
    region: Optional[str]
    expires_in: Optional[int]
    path_style: Optional[bool]
