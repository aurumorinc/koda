# Changelog v0.12.1

## Improvements

* **Refactored File Utilities Import Paths**
  Updated internal import paths to utilize absolute paths rather than relative paths to improve codebase consistency and clarity.
  Commits: [1655df0](https://github.com/aurumorinc/koda/commit/1655df0d), [397515a](https://github.com/aurumorinc/koda/commit/397515a3)

## Other

* **Removed Obsolete Memory Limit Assertion**
  Cleaned up `PlaywrightCrawler` tests by removing an assertion for a memory limit configuration that was previously deprecated and removed from the codebase.
  Commit: [ae945b6](https://github.com/aurumorinc/koda/commit/ae945b64)
