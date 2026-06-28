# Changelog v0.6.0

## Features

* **New Error Handling Classes**
  Introduced `TimeoutError` and `BrowserLaunchError` to provide granular control when handling crawler timeouts and browser initialization failures.
  Commits: [da73c7d](https://github.com/aurumorinc/koda/commit/da73c7d3), [f156ddc](https://github.com/aurumorinc/koda/commit/f156ddca)

## Improvements

* **Exception Hierarchy Refactoring**
  Refactored the internal exception hierarchy to inherit from a unified `Error` base class, simplifying catch blocks and error handling logic for integrations.
  Commits: [da73c7d](https://github.com/aurumorinc/koda/commit/da73c7d3), [f156ddc](https://github.com/aurumorinc/koda/commit/f156ddca)

## Fixes

* **Crawler Execution Timeouts**
  Implemented execution timeouts to prevent crawler hangs, ensuring that long-running processes are terminated appropriately.
  Commits: [da73c7d](https://github.com/aurumorinc/koda/commit/da73c7d3), [f156ddc](https://github.com/aurumorinc/koda/commit/f156ddca)

* **Browser Navigation Error Handling**
  Added specific catch blocks for browser-closed errors during navigation to ensure graceful failure states instead of unhandled exceptions.
  Commits: [da73c7d](https://github.com/aurumorinc/koda/commit/da73c7d3), [f156ddc](https://github.com/aurumorinc/koda/commit/f156ddca)

## Other

* **Stability Testing**
  Added comprehensive end-to-end and unit tests to verify system stability and error handling under high concurrency scenarios.
  Commits: [da73c7d](https://github.com/aurumorinc/koda/commit/da73c7d3), [f156ddc](https://github.com/aurumorinc/koda/commit/f156ddca)
