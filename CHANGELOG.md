# Changelog v0.15.2

## Performance

* **YouTube Scraping Optimization**
  Refactored the profile scraping workflow to utilize in-place SPA navigation via Playwright, eliminating the overhead of separate tab and dialog requests. This change includes the removal of internal helpers `_validate_redirect` and `tab_handler` and optimizes concurrency settings for improved throughput.
  * Commits: [e4bccf6](https://github.com/aurumorinc/koda/commit/e4bccf6e), [90fdf5c](https://github.com/aurumorinc/koda/commit/90fdf5c5), [5b2fa2e](https://github.com/aurumorinc/koda/commit/5b2fa2e0)
