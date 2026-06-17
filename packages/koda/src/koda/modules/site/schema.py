"""Schemas for site crawling."""

from __future__ import annotations
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, HttpUrl

from koda.modules.webhook.schema import WebhookConfig

class ScrapeOptions(BaseModel):
    """Options for scraping individual pages during a crawl."""
    formats: List[str] = Field(default_factory=lambda: ["markdown"])
    onlyMainContent: bool = True
    onlyCleanContent: bool = False
    includeTags: Optional[List[str]] = None
    excludeTags: Optional[List[str]] = None
    maxAge: int = 172800000
    minAge: Optional[int] = None
    headers: Optional[Dict[str, str]] = None
    waitFor: int = 0
    wait_until: str = Field(default="domcontentloaded", alias="waitUntil")
    mobile: bool = False
    skipTlsVerification: bool = True
    timeout: int = Field(default=60000, ge=1000, le=300000)
    parsers: List[Union[str, Dict[str, Any]]] = Field(default_factory=lambda: ["pdf"])
    actions: Optional[List[Dict[str, Any]]] = None
    location: Optional[Dict[str, Any]] = None
    removeBase64Images: bool = True
    blockAds: bool = True
    proxy: str = "auto"
    storeInCache: bool = True
    lockdown: bool = False
    profile: Optional[Dict[str, Any]] = None

class CrawlRequest(BaseModel):
    """Request payload for crawling a site."""
    url: HttpUrl
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
    webhook: Optional[WebhookConfig] = None
    scrapeOptions: ScrapeOptions = Field(default_factory=ScrapeOptions)
    zeroDataRetention: bool = False

class CrawlResponse(BaseModel):
    """Response payload for a crawl request."""
    success: bool
    id: str
    url: str
    total_pages_crawled: Optional[int] = None
