import asyncio
from datetime import datetime, timezone, timedelta
from typing import Any, Mapping, Sequence, Optional
from types import TracebackType

from playwright.async_api import BrowserContext, Page
from crawlee.browsers._browser_controller import BrowserController
from crawlee.browsers._browser_plugin import BrowserPlugin
from crawlee.browsers._types import BrowserType
from crawlee.proxy_configuration import ProxyInfo
from crawlee.crawlers import PlaywrightCrawler as BasePlaywrightCrawler
from crawlee.browsers import BrowserPool
from crawlee.crawlers import PlaywrightCrawlingContext

from koda.config.main import settings
from koda.modules.webhook.schema import WebhookConfig
from koda.modules.webhook.utils import dispatch_webhook
from koda.modules.file.schema import S3Config
from koda.modules.file.service import upload as s3_upload


class KodaBrowserController(BrowserController):
    """A browser controller that simply yields pages from a pre-existing Koda BrowserContext."""
    
    AUTOMATION_LIBRARY = 'playwright'

    def __init__(self, context: BrowserContext):
        self._context = context
        self._pages: list[Page] = []
        self._total_opened_pages = 0
        self._last_page_opened_at = datetime.now(timezone.utc)
        self._is_closed = False

    @property
    def pages(self) -> list[Page]:
        return self._pages.copy()

    @property
    def total_opened_pages(self) -> int:
        return self._total_opened_pages

    @property
    def pages_count(self) -> int:
        return len(self._pages)

    @property
    def last_page_opened_at(self) -> datetime:
        return self._last_page_opened_at

    @property
    def idle_time(self) -> timedelta:
        return datetime.now(timezone.utc) - self._last_page_opened_at

    @property
    def has_free_capacity(self) -> bool:
        # Koda manages capacity globally, we can just allow it
        return True

    @property
    def is_browser_connected(self) -> bool:
        return not self._is_closed

    @property
    def browser_type(self) -> BrowserType:
        return 'chromium'

    async def new_page(
        self,
        browser_new_context_options: Mapping[str, Any] | None = None,
        proxy_info: ProxyInfo | None = None,
    ) -> Page:
        page = await self._context.new_page()
        
        async def _on_close(*args, **kwargs):
            if page in self._pages:
                self._pages.remove(page)

        page.on('close', _on_close)
        
        self._pages.append(page)
        self._total_opened_pages += 1
        self._last_page_opened_at = datetime.now(timezone.utc)
        return page

    async def close(self, *, force: bool = False) -> None:
        """
        We DO NOT close the underlying context because Koda's BrowserSession manages its lifecycle.
        We only close the pages that were opened by this controller.
        """
        self._is_closed = True
        for page in self._pages:
            try:
                await page.close()
            except Exception:
                pass
        self._pages.clear()

class KodaBrowserPlugin(BrowserPlugin):
    """A browser plugin that returns a KodaBrowserController wrapped around a pre-existing Koda context."""
    
    AUTOMATION_LIBRARY = 'playwright'
    
    def __init__(self, context: BrowserContext):
        self._context = context
        self._active = False

    @property
    def active(self) -> bool:
        return self._active

    @property
    def browser_type(self) -> BrowserType:
        return 'chromium'

    @property
    def browser_launch_options(self) -> Mapping[str, Any]:
        return {}

    @property
    def browser_new_context_options(self) -> Mapping[str, Any]:
        return {}

    @property
    def max_open_pages_per_browser(self) -> int:
        return 100000  # Arbitrary high number since Koda manages capacity

    async def __aenter__(self) -> 'KodaBrowserPlugin':
        self._active = True
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_traceback: TracebackType | None) -> None:
        self._active = False

    async def new_browser(self) -> BrowserController:
        return KodaBrowserController(self._context)

class PlaywrightCrawler(BasePlaywrightCrawler):
    """
    A Koda-integrated PlaywrightCrawler that injects the KodaClient and
    wraps the entire crawl execution within Koda's BrowserSession.
    """
    def __init__(
        self,
        *args,
        client: Optional['KodaClient'] = None,  # type: ignore
        **kwargs
    ):
        self.client = client
        
        original_handler = kwargs.pop('request_handler', None)
        args_list = list(args)
        if not original_handler and args_list:
            original_handler = args_list.pop(0)
            
        if original_handler:
            async def koda_wrapped_handler(context: PlaywrightCrawlingContext, *h_args, **h_kwargs) -> None:
                original_push_data = context.push_data
                
                async def custom_push_data(data: Any, *pd_args, **pd_kwargs) -> None:
                    # Execute the original push
                    await original_push_data(data, *pd_args, **pd_kwargs)
                    
                    # Intercept and dispatch webhook if configured globally
                    if settings.webhook_url:
                        from koda.modules.webhook.schema import WebhookConfig
                        from koda.modules.webhook.utils import dispatch_webhook
                        webhook_config = WebhookConfig(
                            url=settings.webhook_url,
                            events=settings.webhook_events,
                            headers=settings.webhook_headers
                        )
                        await dispatch_webhook(webhook_config, "crawl.page", data)
                
                context.push_data = custom_push_data
                return await original_handler(context, *h_args, **h_kwargs)
                
            kwargs['request_handler'] = koda_wrapped_handler
            args = tuple(args_list)

        # We don't initialize the browser_pool here because we need the context
        # which is only available inside the run() async context.
        # But Crawlee might require it. We will override it in run().
        super().__init__(*args, **kwargs)

    async def run(self, *args, **kwargs) -> None:
        """
        Executes the crawl inside a Koda BrowserSession, ensuring that
        we use Koda's invisible-playwright instance and telemetry.
        """
        from koda.modules.browser.service import BrowserSession
        
        async with BrowserSession() as koda_context:
            # We construct a custom BrowserPool using our KodaBrowserPlugin
            # to intercept browser launches and use Koda's context.
            plugin = KodaBrowserPlugin(koda_context)
            
            # Create a custom pool that uses our plugin
            koda_browser_pool = BrowserPool(
                plugins=[plugin],
                # Disable retiring browsers since Koda manages the context lifetime
                retire_browser_after_page_count=0
            )
            
            # Replace the crawler's default browser pool with our custom one
            self._browser_pool = koda_browser_pool

            # The BrowserPool needs to be active
            async with koda_browser_pool:
                await super().run(*args, **kwargs)

            # Post-run: upload dataset to S3 if configured globally
            if settings.s3_bucket_name:
                import json
                import uuid
                
                dataset = await self.get_dataset()
                dataset_data = await dataset.get_data()
                
                if dataset_data and dataset_data.items:
                    json_data = json.dumps(dataset_data.items).encode("utf-8")
                    
                    s3_config_dict = {
                        "bucket": settings.s3_bucket_name,
                        "accessKey": settings.s3_access_key_id,
                        "secretKey": settings.s3_secret_access_key,
                        "endPoint": settings.s3_endpoint_url,
                        "region": settings.s3_region_name,
                    }
                    if settings.s3_addressing_style != "auto":
                        s3_config_dict["pathStyle"] = (settings.s3_addressing_style == "path")
                        
                    s3_config = S3Config(**s3_config_dict)
                    
                    run_id = str(uuid.uuid4())
                    object_name = f"crawlee_datasets/{run_id}.json"
                    
                    # Run the synchronous or async upload
                    s3_upload(json_data, object_name, "application/json", s3_config)
