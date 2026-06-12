from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class S3Config(BaseModel):
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
    model_config = ConfigDict(populate_by_name=True)

    bucket: Optional[str] = None
    access_key: Optional[str] = Field(default=None, alias="accessKey")
    secret_key: Optional[str] = Field(default=None, alias="secretKey")
    endpoint_url: Optional[str] = Field(default=None, alias="endPoint")
    region: Optional[str] = None
    expires_in: Optional[int] = None
    path_style: Optional[bool] = Field(default=None, alias="pathStyle")
