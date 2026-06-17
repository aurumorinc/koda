import asyncio
from typing import Any, AsyncGenerator, Dict, Protocol
from contextlib import asynccontextmanager
from playwright.async_api import Page

from koda.config.main import settings
from koda.integrations.posthog import setup_playwright_transport, setup_network_capture, inject_posthog_monolith, flush_telemetry
from koda.modules.browser.repositories import invisible_playwright
from koda.modules.browser.repositories import cloakbrowser

_LAUNCHERS = {
    "invisible_playwright": invisible_playwright.launch,
    "cloakbrowser": cloakbrowser.launch,
}

from playwright.async_api import BrowserContext

class BrowserTool(Protocol):
    """Protocol for tools that operate on a Playwright Page or Context."""
    async def execute(self, context_or_page: Any, request: Any) -> Any:
        ...

@asynccontextmanager
async def BrowserSession(config: Dict[str, Any] = None) -> AsyncGenerator[BrowserContext, None]:
    """
    Context manager that owns the browser lifecycle.
    Launches the browser, injects telemetry into all pages, and ensures safe teardown.
    """
    if config is None:
        config = {"headless": True}
        
    browser_type = settings.browser or "invisible_playwright"
    launcher = _LAUNCHERS.get(browser_type)
    if not launcher:
        raise ValueError(f"Unsupported browser type: {browser_type}")
        
    # Suppress Playwright's internal TargetClosedError unretrieved futures
    loop = asyncio.get_running_loop()
    original_handler = loop.get_exception_handler()
    
    def custom_exception_handler(loop, context_dict):
        exc = context_dict.get("exception")
        if exc and "TargetClosedError" in str(type(exc).__name__):
            # Ignore TargetClosedError from Playwright's internal tasks (like expose_function)
            return
        if original_handler:
            original_handler(loop, context_dict)
        else:
            loop.default_exception_handler(context_dict)
            
    loop.set_exception_handler(custom_exception_handler)
    
    try:
        async with launcher("", config) as browser:
            # Create a new context from the browser
            context = await browser.new_context()
            
            if settings.posthog_api_key and settings.posthog_host:
                await setup_playwright_transport(context)
                
                async def on_page(page: Page):
                    await setup_network_capture(page, settings.posthog_api_key)
                    await inject_posthog_monolith(page, settings.posthog_api_key, settings.posthog_host)
                    
                context.on("page", on_page)
                
                # Apply to any existing pages
                for page in context.pages:
                    await on_page(page)
                
            try:
                yield context
            finally:
                # Ensure all telemetry is flushed before closing the context
                await flush_telemetry()
                await context.close()
    finally:
        # Restore the original exception handler
        loop.set_exception_handler(original_handler)
