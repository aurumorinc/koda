# Changelog v0.11.0

### Features

* **Navigation: Added Courses tab**
  The navigation list for scraping now includes the `courses` tab, allowing for automated data collection from this new endpoint.
  Commits: [93b9168](https://github.com/aurumorinc/koda/commit/93b9168e), [071234a](https://github.com/aurumorinc/koda/commit/071234a9)

### Improvements

* **URL Handling: Standardized URL construction**
  Refactored internal URL construction logic to remove conditional handling for featured slugs, ensuring more predictable behavior.
  Commits: [93b9168](https://github.com/aurumorinc/koda/commit/93b9168e), [071234a](https://github.com/aurumorinc/koda/commit/071234a9)

* **Screenshot Metadata: Consistent request URLs**
  Updated the screenshot metadata service to utilize the standardized URL construction, ensuring consistent request formatting across the platform.
  Commits: [93b9168](https://github.com/aurumorinc/koda/commit/93b9168e), [071234a](https://github.com/aurumorinc/koda/commit/071234a9)
