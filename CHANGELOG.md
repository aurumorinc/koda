# Changelog v0.10.2

## Improvements

### YouTube Scraping
*   **Centralized tab configuration:** Refactored internal tab management to improve stability during scraping operations. ([50ff1b1](https://github.com/aurumorinc/koda/commit/50ff1b17))
*   **Improved URL resolution:** Enhanced the internal URL resolution logic to better handle dynamic YouTube link structures. ([0b48d75](https://github.com/aurumorinc/koda/commit/0b48d758))
*   **Screenshot helper functions:** Added new utility functions to streamline the extraction and processing of screenshot data from scraped pages. ([a1144a1](https://github.com/aurumorinc/koda/commit/a1144a11))
*   **Handler naming conventions:** Updated internal handler naming conventions across the scraping module to ensure consistency and improve maintainability. ([a1144a1](https://github.com/aurumorinc/koda/commit/a1144a11))

## Performance

### Concurrency
*   **Adjusted default max concurrency:** Updated the default maximum concurrency setting to 10 to improve test suite performance and overall system reliability. ([27eb857](https://github.com/aurumorinc/koda/commit/27eb857e), [1fae610](https://github.com/aurumorinc/koda/commit/1fae6101))
