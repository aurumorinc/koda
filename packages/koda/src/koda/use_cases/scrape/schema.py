from typing import Any, Dict, List, Optional, Union, cast
from pydantic import BaseModel, ConfigDict, Field
from koda.utils.webhook.schema import Webhook
from koda.use_cases.schema import Action

class ScrapeRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    url: str
    formats: List[Union[str, Dict[str, Any]]] = Field(default_factory=lambda: cast(List[Union[str, Dict[str, Any]]], ["markdown", "screenshot"]))
    only_main_content: bool = Field(default=True, alias="onlyMainContent")
    actions: List[Action] = Field(default_factory=list)
    timeout: Optional[int] = None
    s3_resource: Optional[Dict[str, Any]] = None
    webhook: Optional[Webhook] = None

class ScrapeResponse(BaseModel):
    url: str
    markdown: Optional[str] = None
    html: Optional[str] = None
    links: Optional[Dict[str, Any]] = None
    images: Optional[List[Dict[str, Any]]] = None
    screenshot: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    action_results: Optional[Dict[str, Any]] = None
    _screenshot_bytes: Optional[bytes] = None

class ScrapeResult(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
