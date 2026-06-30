# Changelog v0.10.8

### Fixes

* **YouTube Scraping Concurrency Adjustment**
  Decreased the default maximum concurrency for YouTube scraping from 4 to 1 to mitigate rate-limiting issues and prevent resource exhaustion on the host environment.
  * Commits: [d0c78e6](https://github.com/aurumorinc/koda/commit/d0c78e69), [1cd7ec1](https://github.com/aurumorinc/koda/commit/1cd7ec13)
