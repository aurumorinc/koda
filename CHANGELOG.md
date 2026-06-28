# Changelog v0.5.0

## Features

### KodaClient Configuration Overrides
* The `KodaClient` constructor now accepts keyword arguments for runtime configuration overrides, allowing for more flexible client instantiation.
* Configuration inputs are now enforced via Pydantic validation to ensure type safety and schema compliance.
* This change is supported by comprehensive unit tests to verify override behavior.
* Commits: [abf1d05](https://github.com/aurumorinc/koda/commit/abf1d059), [2beb7b1](https://github.com/aurumorinc/koda/commit/2beb7b1f), [9c4d6c2](https://github.com/aurumorinc/koda/commit/9c4d6c2f)
