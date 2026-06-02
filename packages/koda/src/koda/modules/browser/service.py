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
