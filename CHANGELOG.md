# Changelog v0.18.0

## Breaking Changes

*   **Screenshot API parameter updates**
    The `_screenshot` parameter has been renamed to `screenshot` in the API. Additionally, the `max_height_limit` parameter is now `max_height`, and `max_scroll_y` has been removed from `ScrapeYoutubeProfileRequest`.
    *   **Migration:** Update all calls from `_screenshot` to `screenshot`. Rename `max_height_limit` to `max_height` in your function calls. Remove any existing `max_scroll_y` arguments from your `ScrapeYoutubeProfileRequest` objects.
    *   Commit: [6fd4cb6](https://github.com/aurumorinc/koda/commit/6fd4cb6f)

## Improvements

*   **Consolidation of screenshot logic**
    Screenshot logic has been moved into a shared utility, replacing previous router-based handlers to improve maintainability.
    *   Commits: [aa766ae](https://github.com/aurumorinc/koda/commit/aa766ae3), [729fa2c](https://github.com/aurumorinc/koda/commit/729fa2c3), [3a59254](https://github.com/aurumorinc/koda/commit/3a592544)

*   **Explicit event dispatching for image hydration**
    Updated image hydration processes to utilize explicit event dispatching rather than implicit handling.
    *   Commits: [aa766ae](https://github.com/aurumorinc/koda/commit/aa766ae3), [729fa2c](https://github.com/aurumorinc/koda/commit/729fa2c3), [3a59254](https://github.com/aurumorinc/koda/commit/3a592544)

## Infrastructure

*   **Migration to pytest-xdist**
    Replaced custom test orchestration with `pytest-xdist` to enable file-level load distribution during test execution.
    *   Commits: [ab5d83e](https://github.com/aurumorinc/koda/commit/ab5d83ef), [7e21e8a](https://github.com/aurumorinc/koda/commit/7e21e8af)

*   **Core dependency updates**
    Updated `boto3` and `pydantic-settings` to their latest versions and added `pytest-xdist` to the development environment.
    *   Commit: [35c2d85](https://github.com/aurumorinc/koda/commit/35c2d85a)

*   **Removal of unused AWS async libraries**
    Cleaned up the dependency tree by removing unused AWS async libraries and legacy utility modules.
    *   Commit: [35c2d85](https://github.com/aurumorinc/koda/commit/35c2d85a)

## Other

*   **Cleanup of obsolete unit tests**
    Removed redundant tests in `test_service.py` and `test_schema.py` following internal refactoring.
    *   Commit: [7c001e8](https://github.com/aurumorinc/koda/commit/7c001e8b)
