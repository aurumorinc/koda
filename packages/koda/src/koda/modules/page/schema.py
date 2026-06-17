from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict

from koda.modules.file.schema import S3Config
from koda.modules.webhook.schema import WebhookConfig

class Action(BaseModel):
    """Represents an action to be taken on the page before scraping.
    
    Attributes:
        type: The type of action (e.g., 'click', 'wait', 'scroll', 'screenshot', 'write', 'press', 'executeJavascript', 'pdf', 'scrape').
        selector: Optional CSS selector to interact with.
        value: Optional value associated with the action (e.g., text to type or wait duration).
        milliseconds: Optional duration to wait.
        text: Optional text to write.
        key: Optional key to press.
        script: Optional JavaScript code to execute.
        direction: Optional scroll direction ('up' or 'down').
        all: Optional boolean to click all matching elements.
        fullPage: Optional boolean for full page screenshot.
        quality: Optional integer for screenshot quality.
        viewport: Optional dictionary for screenshot viewport.
        format: Optional string for PDF format.
        landscape: Optional boolean for PDF landscape orientation.
        scale: Optional float for PDF scale.
    """
    type: str
    selector: Optional[str] = None
    value: Optional[Any] = None
    milliseconds: Optional[int] = None
    text: Optional[str] = None
    key: Optional[str] = None
    script: Optional[str] = None
    direction: Optional[str] = None
    all: Optional[bool] = None
    fullPage: Optional[bool] = None
    quality: Optional[int] = None
    viewport: Optional[Dict[str, int]] = None
    format: Optional[str] = None
    landscape: Optional[bool] = None
    scale: Optional[float] = None

class ScrapeRequest(BaseModel):
    """Configuration and target for a scraping job.
    
    Attributes:
        url: The URL or local file path to scrape.
        formats: A list of formats to extract, e.g. ["markdown", "screenshot", "metadata", "html", "links", "images"].
        only_main_content: Whether to filter out noise like headers, footers, and sidebars.
        actions: A list of actions to perform on the page before scraping.
        timeout: Maximum time to wait for the scrape job to complete, in milliseconds.
        wait_until: Condition to wait for when navigating (e.g., 'domcontentloaded', 'networkidle', 'load').
        s3_config: Optional S3 configuration dictionary for uploading screenshots.
        webhook: Optional webhook configuration for callbacks.
    """
    model_config = ConfigDict(populate_by_name=True)

    url: str
    formats: List[str] = Field(default_factory=lambda: ["markdown", "screenshot"])
    only_main_content: bool = Field(default=True, alias="onlyMainContent")
    actions: List[Action] = Field(default_factory=list)
    timeout: Optional[int] = None
    wait_until: Optional[str] = Field(default="domcontentloaded", alias="waitUntil")
    s3_config: Optional[S3Config] = None
    webhook: Optional[WebhookConfig] = None

class ScrapeResponse(BaseModel):
    """The result of a scraping job.
    
    Attributes:
        url: The URL that was scraped.
        markdown: The extracted Markdown text, if requested.
        html: The raw HTML content, if requested.
        links: A dictionary of internal and external links, if requested.
        images: A list of image metadata, if requested.
        screenshot: The URL of the uploaded screenshot, if requested and S3 config provided.
        metadata: Extracted metadata tags as a dictionary, if requested.
        error: Any error message that occurred during extraction.
        action_results: Results of actions like screenshots or PDFs.
    """
    url: str
    markdown: Optional[str] = None
    html: Optional[str] = None
    links: Optional[Dict[str, Any]] = None
    images: Optional[List[Dict[str, Any]]] = None
    screenshot: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    action_results: Optional[Dict[str, Any]] = None
