# Changelog v0.15.0

## Features

* **Sync/Async Context Utility**
  Introduced the `is_async_context()` utility to help developers detect the current execution environment, facilitating better handling of synchronous and asynchronous code paths.
  Commits: [6f04705](https://github.com/aurumorinc/koda/commit/6f047059), [bb8c350](https://github.com/aurumorinc/koda/commit/bb8c3503), [175ead6](https://github.com/aurumorinc/koda/commit/175ead62)

* **File Object API Update**
  Updated `File` object interactions to utilize the `presigned_url` property directly instead of the deprecated `get_presigned_url_async()` method, simplifying access to file resources.
  Commits: [6f04705](https://github.com/aurumorinc/koda/commit/6f047059), [bb8c350](https://github.com/aurumorinc/koda/commit/bb8c3503), [175ead6](https://github.com/aurumorinc/koda/commit/175ead62)

## Fixes

* **Browser Configuration Defaulting**
  Resolved a `KeyError` occurring when browser settings were missing by defaulting the configuration to "cloakbrowser".
  Commit: [6d243c4](https://github.com/aurumorinc/koda/commit/6d243c44)
