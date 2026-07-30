# Changelog v0.17.0

## Breaking Changes

* **ScrapeYoutubeProfileRequest parameter update**
  The `ScrapeYoutubeProfileRequest` constructor now includes a `max_scroll_y` parameter. If your implementation uses strict type checking or relies on positional arguments, you must update your constructor calls to accommodate this new parameter. The default value is set to 3072px.

## New Features

* **Added max_scroll_y parameter to ScrapeYoutubeProfileRequest**
  Introduced the `max_scroll_y` field to allow granular control over the vertical scroll distance during YouTube profile scraping operations.
  Commits: [eee40c6](https://github.com/aurumorinc/koda/commit/eee40c6e), [47c536b](https://github.com/aurumorinc/koda/commit/47c536be)

## Improvements

* **Refactored screenshot hydration logic**
  The screenshot logic has been refactored into a dedicated `_screenshot` function to improve maintainability and modularity.
  Commits: [a5bb214](https://github.com/aurumorinc/koda/commit/a5bb214f)

* **Expanded image hydration support**
  Updated the image hydration process to support a wider range of container types, improving compatibility with various data structures.
  Commits: [f548324](https://github.com/aurumorinc/koda/commit/f5483248)
