from typing import Any, Dict, List, Optional, Union, cast
from pydantic import BaseModel, ConfigDict, Field
from koda.utils.webhook.schema import Webhook
from koda.use_cases.schema import Action
from koda.use_cases.scrape.schema import ScrapeRequest, ScrapeResponse


class BatchScrapeRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    urls: Optional[List[str]] = None
    requests: Optional[List[ScrapeRequest]] = None
    formats: List[Union[str, Dict[str, Any]]] = Field(
        default_factory=lambda: cast(
            List[Union[str, Dict[str, Any]]], ["markdown", "screenshot"]
        )
    )
    only_main_content: bool = Field(default=True, alias="onlyMainContent")
    actions: List[Action] = Field(default_factory=list)
    timeout: Optional[int] = None
    s3_resource: Optional[Dict[str, Any]] = None
    webhook: Optional[Webhook] = None
    max_concurrency: Optional[int] = Field(default=None, alias="maxConcurrency")
    ignore_invalid_urls: Optional[bool] = Field(default=True, alias="ignoreInvalidURLs")


class BatchScrapeResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    success: bool
    id: str
    url: Optional[str] = None
    invalid_urls: List[str] = Field(default_factory=list, alias="invalidURLs")
    data: List[ScrapeResponse] = Field(default_factory=list)
