# Changelog v27.0.0

## Breaking Changes

* **Removal of legacy KodaClient scraping and crawling methods**
  The `KodaClient` legacy scraping and crawling methods have been removed in favor of the new `crawl4ai` implementation.
  * **Migration Path:** Replace all instances of `KodaClient` scraping methods with the new `crawl4ai` wrapper classes. Update your integration code to utilize the native wrappers for Crawlee, Stagehand, or Browserforge as appropriate for your specific scraping requirements.
  * **Commits:** [29861c5](https://github.com/aurumorinc/koda/commit/29861c50), [3c03b9e](https://github.com/aurumorinc/koda/commit/3c03b9e2), [af6eb32](https://github.com/aurumorinc/koda/commit/af6eb326)

## Features

* **Lightpanda agent skill integration**
  Added support for Lightpanda as an agent skill, enabling enhanced browser automation capabilities.
  * **Commits:** [19f6d8f](https://github.com/aurumorinc/koda/commit/19f6d8f1)
* **Webhook dispatch decorators**
  Introduced new decorators to facilitate easier webhook dispatching within agent workflows.
  * **Commits:** [4715abb](https://github.com/aurumorinc/koda/commit/4715abb1), [8aa0efc](https://github.com/aurumorinc/koda/commit/8aa0efc5)

## Improvements

* **Standardization of logging telemetry**
  Migrated internal logging to `structlog` and `worldline-python` to ensure consistent telemetry across all services.
  * **Commits:** [03ab903](https://github.com/aurumorinc/koda/commit/03ab9039), [95d92b8](https://github.com/aurumorinc/koda/commit/95d92b8c), [47b88b8](https://github.com/aurumorinc/koda/commit/47b88b8a)

## Infrastructure

* **Initialization of koda-api structure**
  Established the foundational directory and module structure for the new `koda-api` package.
  * **Commits:** [195da66](https://github.com/aurumorinc/koda/commit/195da664)
* **Dependency group updates**
  Refactored and updated dependency groups to support the new API architecture and crawling requirements.
  * **Commits:** [4083994](https://github.com/aurumorinc/koda/commit/40839941), [19a16ee](https://github.com/aurumorinc/koda/commit/19a16eef)
