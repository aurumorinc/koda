from typing import Any, AsyncGenerator, Dict
from contextlib import asynccontextmanager

try:
    from invisible_playwright.async_api import InvisiblePlaywright
except ImportError:
    InvisiblePlaywright = None

@asynccontextmanager
async def launch(user_data_dir: str, config: Dict[str, Any]) -> AsyncGenerator[Any, None]:
    """
    Launch invisible_playwright with a persistent context.
    """
    seed = config.get("seed")
    
    # InvisiblePlaywright is an async context manager
    async with InvisiblePlaywright(
        user_data_dir=user_data_dir,
        seed=seed,
        headless=True
    ) as context:
        yield context
