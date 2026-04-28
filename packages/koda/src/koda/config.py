"""Configuration and models for Koda."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

__all__ = ["ScrapeOptions", "ScrapeResponse", "Action", "KodaError", "ScrapeError", "WebhookConfig"]

class KodaError(Exception):
    """Base exception class for all errors raised by the koda module."""
    pass

class ScrapeError(KodaError):
    """Exception raised when an error occurs during scraping."""
    pass

@dataclass
class Action:
    """Represents an action to be taken on the page before scraping.
    
    Attributes:
        type: The type of action (e.g., 'click', 'wait', 'scroll').
        selector: Optional CSS selector to interact with.
        value: Optional value associated with the action (e.g., text to type or wait duration).
    """
    type: str
    selector: Optional[str] = None
    value: Optional[Any] = None

@dataclass
class WebhookConfig:
    """Configuration for a webhook callback.
    
    Attributes:
        url: The URL to send the webhook to.
        headers: Optional dictionary of headers to include.
        metadata: Optional dictionary of metadata to append to the root payload.
    """
    url: str
    headers: Optional[Dict[str, str]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ScrapeOptions:
    """Configuration options for a scraping job.
    
    Attributes:
        formats: A list of formats to extract, e.g. ["markdown", "screenshot", "metadata"].
        only_main_content: Whether to filter out noise like headers, footers, and sidebars.
        actions: A list of actions to perform on the page before scraping.
        timeout: Maximum time to wait for the scrape job to complete, in milliseconds.
        s3_config: Optional S3 configuration dictionary for uploading screenshots.
        webhook: Optional webhook configuration for callbacks.
    """
    formats: List[str] = field(default_factory=lambda: ["markdown", "screenshot"])
    only_main_content: bool = True
    actions: List[Action] = field(default_factory=list)
    timeout: int = 30000
    s3_config: Optional[Dict[str, Any]] = None
    webhook: Optional[WebhookConfig] = None

@dataclass
class ScrapeResponse:
    """The result of a scraping job.
    
    Attributes:
        url: The URL that was scraped.
        markdown: The extracted Markdown text, if requested.
        screenshot: The URL of the uploaded screenshot, if requested and S3 config provided.
        metadata: Extracted metadata tags as a dictionary, if requested.
        error: Any error message that occurred during extraction.
    """
    url: str
    markdown: Optional[str] = None
    screenshot: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
