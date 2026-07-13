# Changelog v0.13.0

## Breaking Changes

* **Migration to oort-python library**
  We have replaced internal S3, file utilities, and webhook services with the `oort-python` library. This update requires refactoring core scraping functions and updating public API schemas.
  * **Migration Path:**
    * Update all imports from `koda.utils.file` and `koda.utils.webhook` to `oort.file` and `oort.webhook`.
    * Update any code referencing `WebhookRequest` schemas to match the new `oort-python` implementation.
    * Refactor `scrape_youtube_profile`, `crawl`, and `batch_scrape` to utilize the new `webhook_dispatch` decorator pattern.
  * **Commits:** [f20808d](https://github.com/aurumorinc/koda/commit/f20808d7), [db70ce7](https://github.com/aurumorinc/koda/commit/db70ce73), [03726c8](https://github.com/aurumorinc/koda/commit/03726c88)

## Infrastructure

* **Standardized logging implementation**
  Refactored the logging stack to utilize `structlog` directly for improved observability and structured log output.
  * **Commits:** [0736f21](https://github.com/aurumorinc/koda/commit/0736f216)

* **Simplified configuration management**
  Streamlined configuration by inheriting from shared `OortSettings` and `WorldlineSettings` classes, reducing boilerplate in service initialization.
  * **Commits:** [3911b3e](https://github.com/aurumorinc/koda/commit/3911b3e5), [bcfddc1](https://github.com/aurumorinc/koda/commit/bcfddc1a)
