# Changelog v0.10.0

## Breaking Changes

*   **Removal of `tabs` parameter in `ScrapeYoutubeProfileRequest`**
    The `tabs` parameter has been removed from the `ScrapeYoutubeProfileRequest` API. The system now automatically detects active tabs, rendering manual specification unnecessary.
    *   **Migration:** Update all existing calls to `ScrapeYoutubeProfileRequest` to remove the `tabs` argument.
    *   **Commits:** [a5e301d](https://github.com/aurumorinc/koda/commit/a5e301de), [08cfb52](https://github.com/aurumorinc/koda/commit/08cfb527)

## Improvements

*   **Refactored File Handling Utility**
    Refactored internal file handling logic to utilize a new `File` utility class, which now implements automatic serialization for improved consistency.
    *   **Commits:** [f7ca9ec](https://github.com/aurumorinc/koda/commit/f7ca9ec6), [699c573](https://github.com/aurumorinc/koda/commit/699c5737), [eb2dfcd](https://github.com/aurumorinc/koda/commit/eb2dfcd8)

## Fixes

*   **Increased Browser Timeout**
    Increased the default browser timeout from 30,000ms to 300,000ms to better accommodate long-running scraping and automation tasks.
    *   **Commits:** [5876788](https://github.com/aurumorinc/koda/commit/58767884)
