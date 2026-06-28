from typing import Any, Dict, List, Optional, Union, cast
from pydantic import BaseModel, ConfigDict, Field
from koda.utils.webhook.schema import Webhook
from koda.use_cases.schema import Action

class ScrapeOptions(BaseModel):
    formats: List[Union[str, Dict[str, Any]]] = Field(default_factory=lambda: cast(List[Union[str, Dict[str, Any]]], ["markdown"]))
    onlyMainContent: bool = True
    onlyCleanContent: bool = False
    includeTags: Optional[List[str]] = None
    excludeTags: Optional[List[str]] = None
    maxAge: int = 172800000
    minAge: Optional[int] = None
    headers: Optional[Dict[str, str]] = None
    waitFor: int = 0
    mobile: bool = False
    skipTlsVerification: bool = True
    timeout: int = Field(default=60000, ge=1000, le=300000)
    parsers: List[Union[str, Dict[str, Any]]] = Field(default_factory=lambda: cast(List[Union[str, Dict[str, Any]]], ["pdf"]))
    actions: Optional[List[Action]] = None
    location: Optional[Dict[str, Any]] = None
    removeBase64Images: bool = True
    blockAds: bool = True
    proxy: str = "auto"
    storeInCache: bool = True
    lockdown: bool = False
    profile: Optional[Dict[str, Any]] = None

class CrawlRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    url: str
    prompt: Optional[str] = None
    excludePaths: Optional[List[str]] = None
    includePaths: Optional[List[str]] = None
    maxDiscoveryDepth: int = 0
    sitemap: str = "include"
    ignoreQueryParameters: bool = False
    regexOnFullURL: bool = False
    limit: int = 10000
    crawlEntireDomain: bool = False
    allowExternalLinks: bool = False
    allowSubdomains: bool = False
    ignoreRobotsTxt: bool = False
    robotsUserAgent: Optional[str] = None
    delay: Optional[float] = None
    maxConcurrency: int = 10
    webhook: Optional[Webhook] = None
    scrapeOptions: ScrapeOptions = Field(default_factory=ScrapeOptions)
    zeroDataRetention: bool = False

class CrawlResponse(BaseModel):
    success: bool
    id: str
    url: str
    total_pages_crawled: Optional[int] = None
    error: Optional[str] = None
