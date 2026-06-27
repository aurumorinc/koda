import asyncio
from typing import Any, AsyncGenerator, Dict, Protocol, Callable, Awaitable, Optional
from contextlib import asynccontextmanager
from dataclasses import dataclass
import copy
from playwright.async_api import Page

from koda.config.main import settings
from koda.modules.browser.repositories import invisible_playwright
from koda.modules.browser.repositories import cloakbrowser

_LAUNCHERS = {
    "invisible_playwright": invisible_playwright.launch,
    "cloakbrowser": cloakbrowser.launch,
}

from playwright.async_api import BrowserContext, Route

class BrowserTool(Protocol):
    """Protocol for tools that operate on a Playwright Page or Context."""
    async def execute(self, context_or_page: Any, request: Any) -> Any:
        ...

async def _strip_csp_headers(route: Route):
    """
    Intercept document requests and strip Content-Security-Policy headers 
    so inline scripts and eval() execute without restriction.
    """
    if route.request.resource_type != "document":
        return await route.continue_()
    
    try:
        response = await route.fetch()
        headers = response.headers
        filtered_headers = {
            k: v for k, v in headers.items()
            if k.lower() not in ("content-security-policy", "content-security-policy-report-only")
        }
        await route.fulfill(response=response, headers=filtered_headers)
    except Exception:
        # Fallback to continue if fetch fails (e.g. aborted request)
        await route.continue_()

@dataclass(frozen=True)
class CSPStrategy:
    modify_launch_config: Callable[[Dict[str, Any]], Dict[str, Any]]
    context_kwargs: Dict[str, Any]
    intercept: Callable[[BrowserContext], Awaitable[None]]

async def _native_playwright_interceptor(context: BrowserContext) -> None:
    await context.route("**/*", _strip_csp_headers)

def _invisible_playwright_modifier(config: dict) -> dict:
    new_config = copy.deepcopy(config)
    extra_prefs = new_config.get("extra_prefs", {})
    extra_prefs.update({
        "security.csp.enable": False,
        "dom.security.trusted_types.enabled": False
    })
    new_config["extra_prefs"] = extra_prefs
    return new_config

CSP_STRATEGIES = {
    "invisible_playwright": CSPStrategy(
        modify_launch_config=_invisible_playwright_modifier,
        context_kwargs={"bypass_csp": True},
        intercept=_native_playwright_interceptor
    ),
    "default": CSPStrategy(
        modify_launch_config=lambda c: c,
        context_kwargs={"bypass_csp": True},
        intercept=_native_playwright_interceptor
    )
}

@asynccontextmanager
async def BrowserSession(config: Optional[Dict[str, Any]] = None, user_data_dir: str = "") -> AsyncGenerator[BrowserContext, None]:
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
    
    # Only set it if we haven't already (in case of multiple sessions in same loop)
    if not hasattr(loop, "_koda_exception_handler_set"):
        original_handler = loop.get_exception_handler()
        
        def custom_exception_handler(loop, context_dict):
            exc = context_dict.get("exception")
            
            # If the exception is wrapped in a future/task
            if not exc:
                future = context_dict.get("future") or context_dict.get("task")
                if future and hasattr(future, "exception") and not future.cancelled():
                    try:
                        exc = future.exception()
                    except Exception:
                        pass

            if exc and "TargetClosedError" in str(type(exc).__name__):
                # Ignore TargetClosedError from Playwright's internal tasks
                return
                
            if original_handler:
                original_handler(loop, context_dict)
            else:
                loop.default_exception_handler(context_dict)
                
        loop.set_exception_handler(custom_exception_handler)
        setattr(loop, "_koda_exception_handler_set", True)
    
    strategy = CSP_STRATEGIES.get(browser_type, CSP_STRATEGIES["default"])
    config = strategy.modify_launch_config(config)
    
    async with launcher(user_data_dir, config) as browser_or_context:
            # Handle both Browser and persistent BrowserContext yields
            if hasattr(browser_or_context, 'new_context'):
                kwargs = {"permissions": ["geolocation", "notifications"]}
                kwargs.update(strategy.context_kwargs)
                context = await browser_or_context.new_context(**kwargs)
            else:
                context = browser_or_context
                await context.grant_permissions(["geolocation", "notifications"])
            
            # Automatically accept dialogs to prevent hangs
            context.on("dialog", lambda dialog: asyncio.create_task(dialog.accept()))
            
            # Intercept CSP dynamically based on strategy
            await strategy.intercept(context)
            
            from koda.integrations.posthog import setup_playwright_transport, setup_network_capture, inject_posthog_monolith, flush_telemetry

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
