from typing import Any, Dict, List, Optional, Union, cast
from pydantic import BaseModel, ConfigDict, Field
from koda.utils.webhook.schema import Webhook

class ScrapeYoutubeProfileRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    url: str
    formats: List[Union[str, Dict[str, Any]]] = Field(default_factory=lambda: cast(List[Union[str, Dict[str, Any]]], ["markdown"]))
    tabs: Optional[List[str]] = Field(default_factory=lambda: ["home", "videos", "shorts", "streams", "podcasts", "playlists", "community", "store"])
    timeout: int = 300000
    s3_resource: Optional[Dict[str, Any]] = None
    webhook: Optional[Webhook] = None
    max_concurrency: int = Field(default=3, alias="maxConcurrency")

class ScrapeYoutubeProfileResponse(BaseModel):
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
