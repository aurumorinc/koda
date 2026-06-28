# Changelog v0.4.3

## Improvements

### Koda API Refactoring
*   **Enhanced Type Safety:** Refactored core API components to improve type safety across the codebase, reducing potential runtime errors for integrations. (Commits: [04db403](https://github.com/aurumorinc/koda/commit/04db403a))
*   **Async Entrypoint Migration:** Refactored main entrypoints to utilize `async_main` with synchronous wrappers, allowing for better concurrency handling while maintaining backward compatibility for existing synchronous implementations. (Commits: [966afbd](https://github.com/aurumorinc/koda/commit/966afbd6))
*   **Test Suite Optimization:** Optimized the internal test suite execution path to reduce CI/CD build times and improve developer feedback loops. (Commits: [bd4a6e8](https://github.com/aurumorinc/koda/commit/bd4a6e86))
