from typing import Any, AsyncGenerator, Dict
from contextlib import asynccontextmanager

try:
    from cloakbrowser.browser import launch_persistent_context_async
except ImportError:
    launch_persistent_context_async = None

@asynccontextmanager
async def launch(user_data_dir: str, config: Dict[str, Any]) -> AsyncGenerator[Any, None]:
    """
    Launch cloakbrowser with a persistent context.
    """
    # launch_persistent_context_async returns a BrowserContext
    is_headless = config.pop("headless", True)
    context = await launch_persistent_context_async(
        user_data_dir=user_data_dir,
        headless=is_headless,
        **config
    )
    
    try:
        yield context
    finally:
        await context.close()
