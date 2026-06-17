from typing import Any
from playwright.async_api import BrowserContext

from koda.modules.browser.service import BrowserTool

class StagehandTool(BrowserTool):
    """
    Adapter for stagehand that implements the BrowserTool protocol.
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    async def execute(self, context: BrowserContext, request: Any) -> Any:
        """
        Execute a stagehand action using the provided context.
        """
        try:
            from stagehand import Stagehand
        except ImportError:
            raise RuntimeError("stagehand is not installed.")

        page = await context.new_page()
        try:
            # Stagehand natively supports accepting an existing Page object
            stagehand = Stagehand(page=page, **self.kwargs)
            
            action = request.get("action")
            if action == "extract":
                return await stagehand.extract(request.get("instruction"))
            elif action == "act":
                return await stagehand.act(request.get("instruction"))
            elif action == "observe":
                return await stagehand.observe(request.get("instruction"))
            else:
                raise ValueError(f"Unsupported stagehand action: {action}")
        finally:
            await page.close()
