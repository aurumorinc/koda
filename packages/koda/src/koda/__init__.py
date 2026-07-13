"""Koda - Web scraping and extraction engine."""

__version__ = "0.13.0"

from koda import client
from koda import config
from koda import exceptions
from koda import integrations
from koda import utils

from koda.client import KodaClient
from koda.config import Settings, main, settings
from koda.exceptions import Error, ScrapeError, SessionExhaustedError
from koda.integrations import (
    Crawl4AiTool,
    KodaAsyncWebCrawler,
    KodaBrowserController,
    KodaBrowserManager,
    KodaBrowserPlugin,
    KodaPlaywrightCrawler,
    KodaStagehand,
    StagehandTool,
    crawl4ai,
    crawlee,
    flush_telemetry,
    handle_playwright_request,
    inject_posthog_monolith,
    logger,
    posthog,
    setup_network_capture,
    setup_playwright_transport,
    stagehand,
)
from koda.utils import images_are_identical, sanitize_filename
from koda.modules.browser.service import BrowserSession

__all__ = [
    "BrowserSession",
    "Crawl4AiTool",
    "KodaAsyncWebCrawler",
    "KodaBrowserController",
    "KodaBrowserManager",
    "KodaBrowserPlugin",
    "KodaClient",
    "Error",
    "KodaPlaywrightCrawler",
    "KodaStagehand",
    "ScrapeError",
    "SessionExhaustedError",
    "Settings",
    "StagehandTool",
    "client",
    "config",
    "crawl4ai",
    "crawlee",
    "exceptions",
    "flush_telemetry",
    "handle_playwright_request",
    "images_are_identical",
    "inject_posthog_monolith",
    "integrations",
    "logger",
    "main",
    "posthog",
    "sanitize_filename",
    "settings",
    "setup_network_capture",
    "setup_playwright_transport",
    "stagehand",
    "utils",
]
