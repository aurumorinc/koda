# Changelog v0.9.0

## Breaking Changes

*   **Refactored Import Paths for File Handling**
    Import paths for screenshot and PDF handling have been updated to utilize the new `File` abstraction.
    *   **Migration:** Update all import statements referencing the old screenshot or PDF handling modules to use the new `File` utility class.
    *   **Commits:** [19213ce](https://github.com/aurumorinc/koda/commit/19213cee), [43e94e4](https://github.com/aurumorinc/koda/commit/43e94e4c), [5abc1eb](https://github.com/aurumorinc/koda/commit/5abc1eb2)

## Features

*   **Introduction of Unified File Utility Class**
    Introduced a new `File` class to provide a unified interface for managing local temporary files, S3 interactions, and Playwright integration.
    *   **Commits:** [19213ce](https://github.com/aurumorinc/koda/commit/19213cee), [43e94e4](https://github.com/aurumorinc/koda/commit/43e94e4c), [5abc1eb](https://github.com/aurumorinc/koda/commit/5abc1eb2)
