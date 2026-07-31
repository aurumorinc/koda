# Changelog v0.19.0

## Breaking Changes

*   **Reorganization of `koda.use_cases` module**
    The `koda.use_cases` module has been removed. The `Action` schema and `execute_actions` service have been relocated to `koda.modules.page`.
    *   **Migration:** Update all import statements from `koda.use_cases` to `koda.modules.page`.
    *   **Commits:** [46f754e](https://github.com/aurumorinc/koda/commit/46f754e3), [025ba38](https://github.com/aurumorinc/koda/commit/025ba38e), [9f67a20](https://github.com/aurumorinc/koda/commit/9f67a20d)

*   **Rename of `Crawl4AiTool` to `Crawl4AiBrowserTool`**
    The `Crawl4AiTool` class has been renamed to `Crawl4AiBrowserTool` to improve naming consistency.
    *   **Migration:** Update all references and class instantiations of `Crawl4AiTool` to `Crawl4AiBrowserTool` in your codebase.
    *   **Commits:** [0547333](https://github.com/aurumorinc/koda/commit/05473331), [d2fe7fd](https://github.com/aurumorinc/koda/commit/d2fe7fda), [bf5f620](https://github.com/aurumorinc/koda/commit/bf5f6202)

*   **Removal of YouTube profile scraping functionality**
    The `scrape_youtube_profile` use case module and all associated files have been removed from the codebase.
    *   **Migration:** Remove any calls to `scrape_youtube_profile` from your integration logic.
    *   **Commits:** [d2fe7fd](https://github.com/aurumorinc/koda/commit/d2fe7fda), [6c1aabf](https://github.com/aurumorinc/koda/commit/6c1aabf5)
