# Changelog v0.14.1

### Fixes

* **Webhook Serialization**
  Resolved a `RuntimeError` occurring during the serialization of `File` objects within `webhook_dispatch` by adding comprehensive test coverage.
  Commits: [93d495b](https://github.com/aurumorinc/koda/commit/93d495bd), [0812def](https://github.com/aurumorinc/koda/commit/0812def7)

### Infrastructure

* **Dependency Updates**
  Updated core dependencies including `invisible-playwright`, `koda`, `oort-python`, and `playwright` to their latest stable versions.
  Commit: [6d866cd](https://github.com/aurumorinc/koda/commit/6d866cdf)

* **Cleanup of Development Dependencies**
  Removed unused development dependencies to streamline the build environment and reduce package bloat.
  Commit: [6d866cd](https://github.com/aurumorinc/koda/commit/6d866cdf)

### Docs

* **Koda API Documentation**
  Published a comprehensive guide for the Koda web scraping engine, detailing async flow, data schemas, and full endpoint specifications.
  Commit: [727465e](https://github.com/aurumorinc/koda/commit/727465ea)
