# Changelog v27.0.0

## Breaking Changes

*   **Removal of Deprecated Scraping Methods**
    Removed deprecated scraping methods from `KodaClient` and cleaned up unused parameters and actions from the YouTube scraper.
    *   *Migration:* Update all client implementations to remove calls to the deprecated scraping methods.
    *   *Commits:* [12f6d8f](https://github.com/aurumorinc/koda/commit/12f6d8f1), [0c88688](https://github.com/aurumorinc/koda/commit/0c886885)

*   **Configuration and Logging Refactor**
    Removed Sentry integration and global logging initialization; settings are now optional.
    *   *Migration:* Update configuration files to remove Sentry-related settings. If global logging was previously relied upon, implement local logging configuration.
    *   *Commits:* [e47c335](https://github.com/aurumorinc/koda/commit/e47c335e)

## Features

*   **Migration to Crawl4AI and Crawlee**
    Migrated scraping and crawling logic to Crawl4AI and Crawlee, including native browser integrations and updated scraping scripts.
    *   *Commits:* [29861c5](https://github.com/aurumorinc/koda/commit/29861c50), [3c03b9e](https://github.com/aurumorinc/koda/commit/3c03b9e2), [15f4d5d](https://github.com/aurumorinc/koda/commit/15f4d5da)

*   **Webhook Dispatching Implementation**
    Implemented native webhook dispatching to support event-driven architectures.
    *   *Commits:* [de9f800](https://github.com/aurumorinc/koda/commit/de9f800a)

*   **S3 Storage Integration**
    Added native S3 storage integration for persistent data handling.
    *   *Commits:* [4327c99](https://github.com/aurumorinc/koda/commit/4327c99e)

*   **Standardized Crawler Request Handling**
    Implemented standardized request handling across all crawlers to ensure consistent data ingestion.
    *   *Commits:* [70bdd25](https://github.com/aurumorinc/koda/commit/70bdd25e)

## Infrastructure

*   **Logging and Telemetry Migration**
    Migrated standard logging to `structlog` and replaced `python-logging` with `worldline-python` for enhanced observability.
    *   *Commits:* [03ab903](https://github.com/aurumorinc/koda/commit/03ab9039), [95d92b8](https://github.com/aurumorinc/koda/commit/95d92b8c), [47b88b8](https://github.com/aurumorinc/koda/commit/47b88b8a)

## Other

*   **Test Suite Expansion**
    Comprehensive refactor and expansion of unit and E2E tests, including mocking browser sessions and dynamic script imports.
    *   *Commits:* [6ce8b53](https://github.com/aurumorinc/koda/commit/6ce8b53b), [9fca25b](https://github.com/aurumorinc/koda/commit/9fca25b7), [c65ab21](https://github.com/aurumorinc/koda/commit/c65ab213)

*   **Version and Dependency Management**
    Ongoing project configuration, dependency updates, and version alignment across the workspace.
    *   *Commits:* [8471eaa](https://github.com/aurumorinc/koda/commit/8471eaa9), [79d2530](https://github.com/aurumorinc/koda/commit/79d25306), [e3b2d6b](https://github.com/aurumorinc/koda/commit/e3b2d6bd)
