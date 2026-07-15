# Changelog v0.14.0

## Breaking Changes

* **Removal of `s3_resource` parameter from `KodaClient` and request schemas**
  The `s3_resource` parameter has been removed from the `KodaClient` constructor and the `BatchScrapeRequest`, `ScrapeRequest`, and `ScrapeYoutubeProfileRequest` schemas. S3 configuration must now be managed via environment variables.
  * **Migration Guide:** Remove any `s3_resource` arguments from your `KodaClient` instantiations and request object initializations. Ensure your environment is configured with the necessary S3 credentials and settings as required by the updated module-level initialization.
  * **Commits:** [971f007](https://github.com/aurumorinc/koda/commit/971f007d), [c6914f4](https://github.com/aurumorinc/koda/commit/c6914f4c), [dcf33e8](https://github.com/aurumorinc/koda/commit/dcf33e8f)

## Other

* **Removal of S3 integration tests**
  Integration tests that relied on live credentials and external infrastructure have been removed to streamline the test suite.
  * **Commits:** [28a8fb4](https://github.com/aurumorinc/koda/commit/28a8fb46)
