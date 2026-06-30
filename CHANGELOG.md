# Changelog v0.12.0

## Breaking Changes

* **Removal of default "featured" slug in YouTube profile scraper**
  The YouTube profile scraper no longer defaults to the "featured" slug. This change requires all existing implementations to explicitly define the target slug.
  * **Migration:** Update your scraping requests to include the specific slug parameter, as the implicit fallback has been removed.
  * **Commits:** [878bdf7](https://github.com/aurumorinc/koda/commit/878bdf7c), [55caa38](https://github.com/aurumorinc/koda/commit/55caa38b), [cfe4ae0](https://github.com/aurumorinc/koda/commit/cfe4ae0e)

## Improvements

* **Standardization of internal module imports**
  Refactored internal module imports to ensure consistency across the codebase.
  * **Commits:** [104ae01](https://github.com/aurumorinc/koda/commit/104ae01c)
* **Application of consistent code formatting**
  Applied uniform formatting rules across the project to improve maintainability.
  * **Commits:** [cfdd7aa](https://github.com/aurumorinc/koda/commit/cfdd7aa8)
