# Changelog v0.7.0

## Breaking Changes

*   **Configuration schema: `maxConcurrency` renamed to `max_concurrency`**
    The configuration key `maxConcurrency` has been renamed to `max_concurrency` to align with internal naming conventions, and the default value has been increased to 10.
    *   **Migration:** Update all configuration files and environment variable mappings to use the new `max_concurrency` key.
    *   Commit: [2c006d4](https://github.com/aurumorinc/koda/commit/2c006d4b)

*   **API parameter rename: Service function arguments**
    Service function argument names have been updated from class-specific names to generic `request` identifiers to improve consistency across the API.
    *   **Migration:** Update all function calls to use the `request` argument name instead of previous class-named variables.
    *   Commit: [d862210](https://github.com/aurumorinc/koda/commit/d8622101)

## Improvements

*   **Core logic refactoring**
    Centralized core logic and refactored use case schemas into sub-packages to improve maintainability.
    *   Commits: [5f84c52](https://github.com/aurumorinc/koda/commit/5f84c528), [dbc208d](https://github.com/aurumorinc/koda/commit/dbc208d5)

*   **Standardization of S3 configuration**
    Refactored S3 configuration handling to ensure consistency across the codebase.
    *   Commits: [5f84c52](https://github.com/aurumorinc/koda/commit/5f84c528), [dbc208d](https://github.com/aurumorinc/koda/commit/dbc208d5)

*   **Synchronous entry point conversion**
    Converted main entry points to synchronous functions using `asyncio.run` to provide broader compatibility for non-async environments.
    *   Commit: [f3d9f9e](https://github.com/aurumorinc/koda/commit/f3d9f9e9)

## Fixes

*   **Test log suppression**
    Added a logging filter to ignore `TargetClosedError` exceptions during test execution to reduce noise.
    *   Commit: [b45af58](https://github.com/aurumorinc/koda/commit/b45af581)
