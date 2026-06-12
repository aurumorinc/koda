from typing import Any, AsyncGenerator, Dict
from contextlib import asynccontextmanager

from koda.modules.browser.repositories import invisible_playwright
from koda.modules.browser.repositories import cloakbrowser

_LAUNCHERS = {
    "invisible_playwright": invisible_playwright.launch,
    "cloakbrowser": cloakbrowser.launch,
}

@asynccontextmanager
async def launch_browser(browser_type: str, user_data_dir: str, config: Dict[str, Any]) -> AsyncGenerator[Any, None]:
    """
    Launch a browser using the specified adapter.
    """
    launcher = _LAUNCHERS.get(browser_type)
    if not launcher:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    
    async with launcher(user_data_dir, config) as context:
        yield context

async def get_browser(browser_type: str = "invisible_playwright", user_data_dir: str = "", config: Dict[str, Any] = None) -> Any:
    """
    Legacy function to get a browser instance.
    """
    if config is None:
        config = {}
    
    # Map standard playwright browser types to our default launcher
    if browser_type in ["chromium", "firefox", "webkit"]:
        browser_type = "invisible_playwright"
        
    launcher = _LAUNCHERS.get(browser_type)
    if not launcher:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    
    # This is a hack for the monkey patch. It leaks the context.
    # The caller is responsible for closing it.
    context_manager = launcher(user_data_dir, config)
    context = await context_manager.__aenter__()
    context._koda_context_manager = context_manager
    return context
