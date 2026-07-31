# Changelog v0.20.0

## Breaking Changes

* **Refactor of YouTube profile scraper architecture**
  The previous service-based architecture for YouTube profile scraping has been removed and replaced with an inline `Crawlee` `PlaywrightCrawler` implementation.
  * **Migration Path:** If your integration relied on the previous service-based interface, you must update your implementation to utilize the new `Crawlee`-based handler. Ensure all data ingestion logic is updated to leverage the new Pydantic validation models for schema enforcement.

## New Features

* **YouTube Scraper Architecture Migration**
  The YouTube profile scraper has been migrated to use `Crawlee` `PlaywrightCrawler`, enabling multi-tab support, improved SPA navigation handling, and robust data validation via Pydantic.
  * Commits: [6f3346c](https://github.com/aurumorinc/koda/commit/6f3346c4), [00ffa76](https://github.com/aurumorinc/koda/commit/00ffa76e), [13a18db](https://github.com/aurumorinc/koda/commit/13a18db3)

## Other

* **Unit Test Coverage for YouTube Scraper**
  Added comprehensive unit tests for the `scrape_youtube_profile` module, specifically validating request defaults and handler routing logic.
  * Commits: [1996c46](https://github.com/aurumorinc/koda/commit/1996c463)
