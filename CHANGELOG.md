# Changelog

## [2027.0.0](https://github.com/aurumorinc/koda/compare/v2026.1.0...v2027.0.0) (2026-06-12)


### ⚠ BREAKING CHANGES

* Data classes are replaced by Pydantic models, which changes the serialization behavior and may require updates to existing instantiations.
* The Settings class no longer uses os.getenv internally, relying on Pydantic's environment variable handling instead.
* The module exports have changed; the functional API (get_session, release_session, etc.) has been replaced by methods within the SessionService class.
* The cache module no longer exports get/set functions; use the CacheService class instead.
* Requires Python >=3.11 for all environments.
* The KodaClient API no longer requires calling start() or close() and manages external browser context differently.
* The provider field has been removed from the session schema, which may cause errors in code expecting this attribute.
* **utils:** The `extract_metadata` and `html_to_markdown` functions have been removed from `koda.utils`. Any code relying on these utilities must be updated.
* **s3:** The FileService class has been removed. Use the new standalone functions `upload` and `generate_presigned_url` instead.
* **koda:** The ScrapeOptions class is renamed to ScrapeRequest. The WebhookConfig class is removed, and webhook configuration now accepts a generic dictionary.
* **config:** ScrapeResponse.screenshot now returns a string URL instead of bytes.

### Features

* add asynchronous webhook dispatch utility ([726cf5d](https://github.com/aurumorinc/koda/commit/726cf5d67d98af0eb804ad3aeae38ca672831e52))
* add browser stealth and analytics infrastructure ([02b6cef](https://github.com/aurumorinc/koda/commit/02b6cef30373d9408241b7d7d5d69e4a54fa52c8))
* add cache repository documentation ([7102c9f](https://github.com/aurumorinc/koda/commit/7102c9fbccbb8a292cd73fce0fe7472e7cbea813))
* add cache repository documentation ([8918eb4](https://github.com/aurumorinc/koda/commit/8918eb4b5dc46e3a241c4542722c11761c215253))
* add centralized configuration settings ([2de04d9](https://github.com/aurumorinc/koda/commit/2de04d9694758f1bce3757142944955466467fd7))
* add centralized configuration settings ([ed76d98](https://github.com/aurumorinc/koda/commit/ed76d9878d5411b8a4fbb7e1ce9c5eb980c612c6))
* add comprehensive unit and integration tests ([86f590a](https://github.com/aurumorinc/koda/commit/86f590a39592d843f9091b730bbacf304149c767))
* add consul lock repository implementation ([d3e7a96](https://github.com/aurumorinc/koda/commit/d3e7a968d635cf3a71ac8df843ed2ea0d4a1707e))
* add crawl script for Windmill ([e713c59](https://github.com/aurumorinc/koda/commit/e713c5998c8e3b87d67fd5c21d117e218674fcf0))
* add documentation for raw apps and skills ([f532697](https://github.com/aurumorinc/koda/commit/f53269748ae9b68462deaf69fbf1f7603cf9bf03))
* add headless config and legacy browser helper ([4dd5332](https://github.com/aurumorinc/koda/commit/4dd5332af69604d81034ac9736083bfd716f7223))
* add IMAP email fetching functionality ([d33ccb1](https://github.com/aurumorinc/koda/commit/d33ccb1299f1b3f6c4bfb4895cbee30111fe8134))
* add JMAP email fetcher ([864d348](https://github.com/aurumorinc/koda/commit/864d3480750ba70e5e614a1c3ce958c46c01691a))
* add Koda scrape script ([2722c38](https://github.com/aurumorinc/koda/commit/2722c38badca36b655d49001d59e9d1dce1dc0ed))
* add OpenTelemetry logging support ([18e49cd](https://github.com/aurumorinc/koda/commit/18e49cdb7dfab32a138a6e55cac1af50f0e425a6))
* add OpenTelemetry logging support ([780e8e4](https://github.com/aurumorinc/koda/commit/780e8e49e3baf69c43d230a839579a08d5c8b9fd))
* add posthog monolith asset ([dab7a67](https://github.com/aurumorinc/koda/commit/dab7a6700fc98aef9a3af5c7629d4fe9aab40f74))
* add Redis-based locking repository ([b1031b9](https://github.com/aurumorinc/koda/commit/b1031b975fce598c99d08d6fc253c72a184fce63))
* add session schema and model ([410b9b3](https://github.com/aurumorinc/koda/commit/410b9b39d84b2da2d8784f05667e2c8fb521f2a9))
* add site crawling service and schemas ([2af4a20](https://github.com/aurumorinc/koda/commit/2af4a20b36c00af919f26819586322ec618229ac))
* add Windmill storage repository ([2acbd56](https://github.com/aurumorinc/koda/commit/2acbd5673b78e36b18bbb29fe764439cc83f7bc0))
* add windmill trace context to logger ([56915c7](https://github.com/aurumorinc/koda/commit/56915c7ebd490d47ccacb5966c413d82dacf9491))
* **client:** implement KodaClient for web scraping ([4772663](https://github.com/aurumorinc/koda/commit/47726637abda5ab0d912758fd853277e943055fa))
* **client:** refactor scrape method and add file support ([130b199](https://github.com/aurumorinc/koda/commit/130b19982f538bcf3ba51e5bce441dbec52c1ef2))
* **config:** add webhook and s3 config support ([9cbb1bc](https://github.com/aurumorinc/koda/commit/9cbb1bc7dd13a306aee8353968696f52953f2375))
* expand settings configuration ([3f9e3c4](https://github.com/aurumorinc/koda/commit/3f9e3c453d92eab5d607be9da76f806a05cb7814))
* export file module components ([b45bbe9](https://github.com/aurumorinc/koda/commit/b45bbe90662965dfaeb33b0582eea40ac91a3b8c))
* **file:** add S3 service for file uploads ([c999af7](https://github.com/aurumorinc/koda/commit/c999af79b3c58fdad825c24825d511c019921225))
* implement browser service for adapter pattern ([f770269](https://github.com/aurumorinc/koda/commit/f7702691d2c84dc0e4c4601e5a94ab9d13f2b530))
* implement s3 browser profile persistence ([a9da8a5](https://github.com/aurumorinc/koda/commit/a9da8a530dc9ad63b556a17549adfb4a0d34f83e))
* implement session service for management and MFA ([af47c8c](https://github.com/aurumorinc/koda/commit/af47c8c4297584b63c22023d904c26472d8808a4))
* implement Windmill cache module ([768cc99](https://github.com/aurumorinc/koda/commit/768cc99b60aeef946635c92891da06d9b1536328))
* **koda:** add configuration and model definitions ([4677c61](https://github.com/aurumorinc/koda/commit/4677c61f54b3ffabf82335e2cf3a4442db047e65))
* **koda:** add custom exception classes ([938dc4c](https://github.com/aurumorinc/koda/commit/938dc4c62c5396aa40168da05a2d47ebc3e747d0))
* **koda:** add page extraction and screenshotting service ([b9a8071](https://github.com/aurumorinc/koda/commit/b9a807171a8aa9dd645e0e55d844cb37c239914f))
* **koda:** add S3Config TypedDict for storage ([95cafb2](https://github.com/aurumorinc/koda/commit/95cafb20c5acfc3fa4783da51fab321120e7c663))
* **koda:** add Scraper service for page extraction ([770471e](https://github.com/aurumorinc/koda/commit/770471e84331f05bf75647b214b08690207c6a93))
* **koda:** add utility functions for image and text ([da464fe](https://github.com/aurumorinc/koda/commit/da464fe706a2ff7a10fdfa1d9d7ddb9720a0d40a))
* **koda:** add webhook service for callbacks ([eefb9e3](https://github.com/aurumorinc/koda/commit/eefb9e37e3afbd55bea99f73432ebdaee49ac833))
* **koda:** add WebhookConfig schema ([bd7e14f](https://github.com/aurumorinc/koda/commit/bd7e14ff9b8208fbbd0d9ca6d09608cb5122ae6f))
* **koda:** export WebhookConfig in package init ([e7a58d0](https://github.com/aurumorinc/koda/commit/e7a58d0e2246c94f4164f26b22f5a543aa7ca4d6))
* **koda:** expose public API in package __init__ ([8e50062](https://github.com/aurumorinc/koda/commit/8e50062577816f7c38b288b619a2e97463978079))
* **scrape:** add S3 upload support for screenshots ([e7ae2ce](https://github.com/aurumorinc/koda/commit/e7ae2ce4d3aa7115ce6b6df81fd4c9b27678f5e2))
* update PageAction and ScrapeResponse schemas ([9bd876e](https://github.com/aurumorinc/koda/commit/9bd876edc1c6a7200da86ebb37d6ad48b8768b2c))


### Bug Fixes

* remove provider field from session schema ([e4a10e2](https://github.com/aurumorinc/koda/commit/e4a10e2a6d88a2e203d4dbd42da78f1abacafac3))


### Documentation

* add instructions for Windmill AI agent ([a3f86f5](https://github.com/aurumorinc/koda/commit/a3f86f51fffeddf1106e8da366861d2c42026402))
* add pull request template ([3163e21](https://github.com/aurumorinc/koda/commit/3163e21124a0c3b1e8348eab227605dec90165e7))
* add pull request template ([3785e1f](https://github.com/aurumorinc/koda/commit/3785e1fa1e6e89ddda7faa534591b224fc49bdd7))
* add reference to AGENTS.md ([d66ea6f](https://github.com/aurumorinc/koda/commit/d66ea6fea2012dd1d5b947f74e53dde73302682b))


### Miscellaneous Chores

* update dependencies and project config ([ed3e357](https://github.com/aurumorinc/koda/commit/ed3e3571af4594fa9a7f05063635102d37a8cfcf))


### Code Refactoring

* convert cache service to class-based structure ([357ae7c](https://github.com/aurumorinc/koda/commit/357ae7c3b06a7c938b712e5703f9706435d15530))
* **koda:** rename ScrapeOptions to ScrapeRequest ([1781ef8](https://github.com/aurumorinc/koda/commit/1781ef89ee4aee6e5cec3d89ece13da6f49401a3))
* migrate data structures to pydantic models ([255fd9f](https://github.com/aurumorinc/koda/commit/255fd9f606696bcf6bc1267ea7b6e0010ad99a52))
* migrate settings to pydantic-settings ([c560047](https://github.com/aurumorinc/koda/commit/c560047d54845c171b32bd749b09d62cbc0a60e1))
* refactor session service into a class ([634aa61](https://github.com/aurumorinc/koda/commit/634aa611ab5e0c9422ece883b0e86fca9d5b1103))
* rewrite KodaClient to decouple from Playwright ([e565337](https://github.com/aurumorinc/koda/commit/e565337870c0e2306f62bbc96263a301b5e72fe4))
* **s3:** decouple file service into standalone functions ([acf2444](https://github.com/aurumorinc/koda/commit/acf24444c390df25be6949b6a7e9bec3b296b47c))
* **utils:** remove unused metadata and HTML tools ([c985865](https://github.com/aurumorinc/koda/commit/c985865cb4bc981ce5b6489652370ff8ca245234))
