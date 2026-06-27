# Changelog v0.4.0

## Breaking Changes

*   **Architecture Refactor: Migration to Class-Based Services and Pydantic Models**
    *   The codebase has been refactored from procedural functions to class-based services (`SessionService`, `ScrapeJob`, `CacheService`) and Pydantic models. Legacy scraping logic and deprecated configuration parameters have been removed.
    *   **Migration Guide:** Update all code references from procedural function calls to the new class-based service patterns. Replace legacy configuration keys with the new Pydantic-validated configuration schema.
    *   Commits: [283](https://github.com/aurumorinc/koda/commit/283), [282](https://github.com/aurumorinc/koda/commit/282), [281](https://github.com/aurumorinc/koda/commit/281)

## Features

*   **Browser & Crawler Integration**
    *   Migrated core engine to Crawlee and Crawl4Ai with a new `BrowserSession` abstraction.
    *   Added support for batch scraping, YouTube scraping, and S3/Webhook integrations.
    *   Commits: [328](https://github.com/aurumorinc/koda/commit/328), [305](https://github.com/aurumorinc/koda/commit/305), [304](https://github.com/aurumorinc/koda/commit/304)

## Improvements

*   **Observability Infrastructure**
    *   Migrated logging and tracing infrastructure to `structlog` and OpenTelemetry for improved observability.
    *   Commits: [330](https://github.com/aurumorinc/koda/commit/330), [312](https://github.com/aurumorinc/koda/commit/312), [24](https://github.com/aurumorinc/koda/commit/24)
*   **Test Suite Expansion**
    *   Expanded integration and E2E testing coverage, including the implementation of mock servers and browser session mocking.
    *   Commits: [49](https://github.com/aurumorinc/koda/commit/49), [48](https://github.com/aurumorinc/koda/commit/48), [47](https://github.com/aurumorinc/koda/commit/47)

## Infrastructure

*   **Project Standards and Dependency Management**
    *   Migrated to `runemodules` and removed git submodules.
    *   Updated dependency management to PDM.
    *   Commits: [144](https://github.com/aurumorinc/koda/commit/144), [143](https://github.com/aurumorinc/koda/commit/143), [135](https://github.com/aurumorinc/koda/commit/135)
