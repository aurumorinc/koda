# Changelog v0.8.0

## Breaking Changes

* **YouTube Scraper API Data Format Change**
  The YouTube scraper API has been redesigned to return base64 screenshot data instead of markdown or HTML content.
  * **Migration Path:** Update your integration logic to process base64 image strings. You must also review the new configuration options for headless/pixel substitution to ensure compatibility with your specific environment.

## Features

* **YouTube Scraper Redesign**
  The scraper has been completely overhauled to support network-aware scrolling and targeted tab screenshots, returning base64 data.
  * **Commits:** [b4b7cda](https://github.com/aurumorinc/koda/commit/b4b7cdab), [8e7fae2](https://github.com/aurumorinc/koda/commit/8e7fae2d), [f8bf53c](https://github.com/aurumorinc/koda/commit/f8bf53cf)

## Fixes

* **WebRender Indentation Correction**
  Fixed an issue with WebRender indentation to ensure proper configuration parsing.
  * **Commit:** [658eab8](https://github.com/aurumorinc/koda/commit/658eab87)
* **Configuration Alias Support**
  Added support for multiple aliases (environment variables and field names) for configuration settings.
  * **Commit:** [a81636e](https://github.com/aurumorinc/koda/commit/a81636e1)
* **Linux WebRender Support**
  Enabled WebRender support specifically for Linux environments.
  * **Commit:** [a689319](https://github.com/aurumorinc/koda/commit/a6893194)
* **KodaClient Pixel Substitution**
  Disabled pixel substitution by default in KodaClient to align with the new scraper architecture.
  * **Commit:** [a689319](https://github.com/aurumorinc/koda/commit/a6893194)

## Docs

* **AI Coding Standards Reference**
  Added `AGENTS.md` to the repository, providing a comprehensive reference for Clean Architecture, Domain-Driven Design (DDD), Python standards, and infrastructure patterns.
  * **Commit:** [95b38ed](https://github.com/aurumorinc/koda/commit/95b38ed6)
