# Changelog v0.16.0

## Breaking Changes

* **Removal of `max_concurrency` parameter in `scrape_youtube_profile`**
  The `max_concurrency` parameter has been removed from the `scrape_youtube_profile` method signature. This parameter is no longer supported in the request schema.
  *Migration:* Remove the `max_concurrency` argument from any existing calls to `scrape_youtube_profile`.
  *Commits:* [c26e28b](https://github.com/aurumorinc/koda/commit/c26e28b8), [1d173ed](https://github.com/aurumorinc/koda/commit/1d173ede), [bfed37d](https://github.com/aurumorinc/koda/commit/bfed37d6)

## Features

* **Added `_hydrate_all_images` for eager loading**
  Introduced the `_hydrate_all_images` method to force eager loading of lazy-loaded thumbnails, ensuring that screenshots capture the complete visual state of the page.
  *Commits:* [88db00f](https://github.com/aurumorinc/koda/commit/88db00f1)

## Improvements

* **Enhanced YouTube Profile Scraping reliability**
  Updated the scraping logic for YouTube profiles to include increased wait times and network idle waits, reducing flakiness in data extraction.
  *Commits:* [c26e28b](https://github.com/aurumorinc/koda/commit/c26e28b8), [1d173ed](https://github.com/aurumorinc/koda/commit/1d173ede), [bfed37d](https://github.com/aurumorinc/koda/commit/bfed37d6)
