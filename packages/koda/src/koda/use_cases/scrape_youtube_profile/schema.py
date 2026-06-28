from typing import Any, Dict, List, Optional, Union, cast
from pydantic import BaseModel, ConfigDict, Field
from koda.utils.webhook.schema import Webhook

class ScrapeYoutubeProfileRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    url: str
    formats: List[Union[str, Dict[str, Any]]] = Field(default_factory=lambda: cast(List[Union[str, Dict[str, Any]]], ["markdown"]))
    timeout: int = 300000
    s3_resource: Optional[Dict[str, Any]] = None
    webhook: Optional[Webhook] = None
    max_concurrency: int = 10

class ScrapeYoutubeProfileResponse(BaseModel):
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
