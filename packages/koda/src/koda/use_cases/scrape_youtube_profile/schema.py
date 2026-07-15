from typing import Any, Dict, List, Optional, Union, cast
from pydantic import BaseModel, ConfigDict, Field
from oort.webhook.schema import WebhookRequest

__all__ = ["ScrapeYoutubeProfileRequest", "ScrapeYoutubeProfileResponse"]
class ScrapeYoutubeProfileRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    url: str
    formats: List[Union[str, Dict[str, Any]]] = Field(
        default_factory=lambda: cast(List[Union[str, Dict[str, Any]]], ["markdown"])
    )
    timeout: int = 300000
    webhook: Optional[WebhookRequest] = None
    max_concurrency: int = Field(default=1, alias="maxConcurrency")


class ScrapeYoutubeProfileResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
