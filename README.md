# Koda

Koda is a resilient, high-performance browser automation and RPA framework.

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
