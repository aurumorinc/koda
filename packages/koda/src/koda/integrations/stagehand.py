from typing import Any
from playwright.async_api import BrowserContext

from koda.modules.browser.service import BrowserTool

try:
    from stagehand import Stagehand as BaseStagehand
except ImportError:
    BaseStagehand = object

class KodaStagehand(BaseStagehand):  # type: ignore[misc]
    """
    A custom Stagehand wrapper that routes browser management through Koda's
    infrastructure if a `client` is provided.
    """
    def __init__(self, **kwargs):
        self.client = kwargs.pop("client", None)
        self._koda_session = None
        self._koda_context = None
        if BaseStagehand is not object:
            super().__init__(**kwargs)

    async def init(self, *args, **kwargs):
        if self.client and not getattr(self, "page", None):
            from koda.modules.browser.service import BrowserSession
            self._koda_session = BrowserSession()
            self._koda_context = await self._koda_session.__aenter__()
            self.page = await self._koda_context.new_page()
            self.context = self._koda_context
            
        if BaseStagehand is not object and hasattr(super(), "init"):
            await super().init(*args, **kwargs)

    async def close(self, *args, **kwargs):
        if BaseStagehand is not object and hasattr(super(), "close"):
            await super().close(*args, **kwargs)
        if self._koda_session:
            await self._koda_session.__aexit__(None, None, None)
            self._koda_session = None
            self._koda_context = None

if BaseStagehand is not object:
    import sys
    import stagehand
    stagehand.Stagehand = KodaStagehand  # type: ignore[attr-defined]
    if 'stagehand' in sys.modules:
        sys.modules['stagehand'].Stagehand = KodaStagehand  # type: ignore[attr-defined]

class StagehandTool(BrowserTool):
    """
    Adapter for stagehand that implements the BrowserTool protocol.
    DEPRECATED: Use the native KodaStagehand wrapper instead.
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    async def get_stagehand(self, page: Any) -> Any:
        try:
            from stagehand import Stagehand
        except ImportError:
            raise RuntimeError("stagehand is not installed.")
        return Stagehand(page=page, **self.kwargs)  # type: ignore[call-arg]

    async def execute(self, context_or_page: Any, request: Any) -> Any:
        """
        Execute a stagehand action using the provided context.
        """
        try:
            from stagehand import Stagehand
        except ImportError:
            raise RuntimeError("stagehand is not installed.")

        page = await context_or_page.new_page()
        try:
            # Stagehand natively supports accepting an existing Page object
            stagehand = Stagehand(page=page, **self.kwargs)  # type: ignore[call-arg]
            
            action = request.get("action")
            if action == "extract":
                return await stagehand.extract(request.get("instruction"))  # type: ignore[attr-defined]
            elif action == "act":
                return await stagehand.act(request.get("instruction"))  # type: ignore[attr-defined]
            elif action == "observe":
                return await stagehand.observe(request.get("instruction"))  # type: ignore[attr-defined]
            else:
                raise ValueError(f"Unsupported stagehand action: {action}")
        finally:
            await page.close()
