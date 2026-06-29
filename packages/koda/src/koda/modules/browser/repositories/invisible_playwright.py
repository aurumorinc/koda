from typing import Any, AsyncGenerator, Dict
from contextlib import asynccontextmanager

try:
    from invisible_playwright.async_api import InvisiblePlaywright
except ImportError:
    InvisiblePlaywright = None

if InvisiblePlaywright is not None:
    class KodaInvisiblePlaywright(InvisiblePlaywright):
        def _default_context_kwargs(self) -> Dict[str, Any]:
            kwargs = super()._default_context_kwargs()
            # Force Playwright's native CSP bypass on the persistent context
            kwargs["bypass_csp"] = True
            return kwargs

@asynccontextmanager
async def launch(user_data_dir: str, config: Dict[str, Any]) -> AsyncGenerator[Any, None]:
    """
    Launch invisible_playwright with a persistent context.
    """
    seed = config.get("seed")
    headless = config.get("headless", False)
    extra_prefs = dict(config.get("extra_prefs") or {})
    
    # Disable canvas/webgl pixel substitution if screenshot compatibility is needed
    if not config.get("substitute_pixels", True):
        extra_prefs["zoom.stealth.canvas.substitute_pixels"] = False
        extra_prefs["zoom.stealth.webgl.substitute_pixels"] = False

        import sys
        if sys.platform.startswith("linux"):
            extra_prefs["gfx.webrender.all"] = True
            extra_prefs["gfx.webrender.force-disabled"] = False
            extra_prefs["gfx.webrender.software"] = True

    if InvisiblePlaywright is None:
        raise RuntimeError("invisible_playwright is not installed.")

    # InvisiblePlaywright is an async context manager
    async with KodaInvisiblePlaywright(
        seed=seed,
        headless=headless,
        extra_prefs=extra_prefs
    ) as context:
        yield context
