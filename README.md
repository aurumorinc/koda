# Koda

Koda is a resilient, high-performance browser automation and RPA framework.

## Crawlee Integration

Koda natively integrates with [Apify's Crawlee for Python](https://crawlee.dev/python/) to provide highly resilient web crawling. We export a customized `PlaywrightCrawler` that acts as a drop-in replacement for the native Crawlee crawler.

### Why use Koda's PlaywrightCrawler?
Unlike the standalone Crawlee implementation, Koda's `PlaywrightCrawler`:
- **Routes through Koda's `BrowserSession`**: All page provisioning uses Koda's internal lifecycle management. This means your Crawlee spiders automatically benefit from **`invisible-playwright`** (stealth bypasses) and **PostHog Telemetry**.
- **Shared Context**: It prevents duplicate unmanaged Playwright instances from spinning up, saving memory and keeping proxy/CSP bypass strategies intact.
- **`KodaClient` Access**: Internal route handlers have direct access to your `KodaClient` via `context.crawler.client`, allowing you to seamlessly upload scraped screenshots to S3 or dispatch Webhooks mid-crawl.

### Usage

```python
import asyncio
from koda.client import KodaClient
from koda.integrations.crawlee import PlaywrightCrawler
from crawlee.crawlers import PlaywrightCrawlingContext

async def main():
    # 1. Initialize KodaClient as usual (handles configuration, S3, Webhooks, Caching)
    async with KodaClient() as client:
        
        # 2. Initialize the Koda crawler instead of the native one
        # We pass the client instance so we can access it inside our routes
        crawler = PlaywrightCrawler(
            client=client,
            max_requests_per_crawl=50,
        )

        @crawler.router.default_handler
        async def handler(context: PlaywrightCrawlingContext) -> None:
            context.log.info(f"Processing {context.request.url} via Koda Engine")
            
            # The 'context.page' is backed by Koda's invisible-playwright stealth context
            screenshot_bytes = await context.page.screenshot(full_page=True)
            
            # Using KodaClient's file service to upload to S3 directly from the router
            # Note: client is accessible via the crawler object
            # s3_url = await context.crawler.client.file.upload(...)
            
            await context.push_data({
                'url': context.request.url,
                'title': await context.page.title(),
            })

        await crawler.run(['https://www.youtube.com/@mkbhd'])

if __name__ == '__main__':
    asyncio.run(main())
```

## Stagehand Cache Repository

Koda includes a unified, asynchronous cache repository designed to integrate seamlessly with **Stagehand**'s auto-caching and self-healing capabilities. This allows Stagehand to persist resolved XPaths offsite (e.g., in Windmill's state storage) across distributed worker executions, achieving 0ms LLM latency on subsequent runs.

### Configuration

The cache repository is configured via environment variables or the centralized settings in [`packages/koda/src/koda/config/main.py`](packages/koda/src/koda/config/main.py):

- `CACHE_REPOSITORY`: The active cache backend. Defaults to `"windmill"`.
- `CACHE_PREFIX`: A prefix prepended to all cache keys to prevent collisions. Defaults to `"koda:cache:"`.
- `WINDMILL_WORKSPACE`: The active Windmill workspace ID (required for Windmill caching).
- `WINDMILL_TOKEN`: The Windmill API token (required for Windmill caching).
- `WINDMILL_BASE_URL`: The base URL of your Windmill instance. Defaults to `"https://app.windmill.dev"`.

### Usage

#### 1. Direct Cache Usage

You can access the unified async cache object through the `KodaClient`:

```python
from koda.client import KodaClient

async def main():
    async with KodaClient() as client:
        # Set a value in the cache
        await client.cache.set("my_key", {"xpath": "//button[@id='login']"})

        # Retrieve a value from the cache
        value = await client.cache.get("my_key")
        print(value)  # {'xpath': "//button[@id='login']"}
```

#### 2. Integrating with Stagehand

Stagehand accepts a custom cache provider that implements asynchronous `get` and `set` methods. Since Koda's cache adapter is purely asynchronous and follows this exact interface, you can pass it directly to Stagehand via the `KodaClient`:

```python
from stagehand import Stagehand
from koda.client import KodaClient

async def run_automation():
    async with KodaClient() as client:
        # Initialize Stagehand with Koda's unified cache
        stagehand = Stagehand(
            cache=client.cache,  # Pass the Koda cache adapter directly
            model="gpt-4o"
        )

    # Stagehand will automatically use the cache to store and retrieve resolved selectors
    await stagehand.init()
    
    # 1st Run: Stagehand queries LLM, resolves XPath, and caches it in Windmill
    # 2nd Run: Stagehand fetches XPath from Windmill instantly (0ms LLM latency)
    await stagehand.act("click the login button")
    
    await stagehand.close()
```

### Windmill State Persistence

When running inside a Windmill worker, the Windmill cache backend automatically reads the `WM_STATE_PATH` or `WM_STATE_PATH_FILE` environment variables to locate the script's scoped state resource. It fetches, merges, and updates the state dictionary atomically using Windmill's REST API, ensuring offsite persistence without any manual setup.
