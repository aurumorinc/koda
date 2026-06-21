# Changelog

All notable changes to this project will be documented in this file.

## [26.6.21] - 2026-06-21

### 🚀 Features

- Add python-logging runemodule

### 📚 Documentation

- Add agent skill documentation for cloakbrowser
- Update crawl4ai module structure documentation
- Add AST map to SKILL.md
- Clean up posthog-js directory structure documentation
- Update python-logging AST map
- Update stagehand skill documentation
- Update windmill module documentation

### ⚙️ Miscellaneous Tasks

- Update gitignore with new paths

### Build

- [**breaking**] Migrate submodules to runemodules configuration

## [26.6.20] - 2026-06-21

### 🚀 Features

- Add flexible CSP management strategies

### 🚜 Refactor

- Remove default CSP preferences from playwright

### ⚙️ Miscellaneous Tasks

- Release 26.6.20

## [26.6.19] - 2026-06-21

### 🚀 Features

- Enhance browser session configuration
- Add error tracking to page action execution

### 🧪 Testing

- Add integration test for CSP bypass

### ⚙️ Miscellaneous Tasks

- Release 26.6.19

## [26.6.18] - 2026-06-20

### 🚀 Features

- Enhance action handling and request support

### 🧪 Testing

- Add e2e and update integration tests for youtube scout

### ⚙️ Miscellaneous Tasks

- Release 26.6.18

## [26.6.17] - 2026-06-19

### 🚀 Features

- Add batch scraping capability
- Make headless mode configurable for cloakbrowser
- Add batch scrape functionality

### 🧪 Testing

- Add integration tests for batch scraping and youtube scraping

### ⚙️ Miscellaneous Tasks

- Release 26.6.17

## [26.6.16] - 2026-06-18

### 🚀 Features

- Add execute_stream method to crawl4ai integration

### 🚜 Refactor

- Migrate crawler to native crawl4ai strategies

### 🧪 Testing

- Update crawl integration tests to streaming

### ⚙️ Miscellaneous Tasks

- Release 26.6.16

## [26.6.15] - 2026-06-18

### 🐛 Bug Fixes

- Add timeout to page evaluation
- Handle exceptions wrapped in futures

### 🚜 Refactor

- [**breaking**] Remove wait_until configuration
- Remove unused wait_until scrape option

### 🧪 Testing

- Fail tests on unhandled asyncio exceptions

### ⚙️ Miscellaneous Tasks

- Release 26.6.15

## [26.6.14] - 2026-06-17

### 🚀 Features

- Add wait_until option to page schema
- Add wait_until option to site scraper

### 🐛 Bug Fixes

- Prevent errors when page closes during event
- Prevent multiple exception handler overrides

### ⚙️ Miscellaneous Tasks

- Release 26.6.14

## [26.6.13] - 2026-06-17

### ⚙️ Miscellaneous Tasks

- Remove agent and roo configuration rules
- Release 26.6.13

## [26.6.12] - 2026-06-17

### 🐛 Bug Fixes

- Set default values for browser settings

### ⚙️ Miscellaneous Tasks

- Release 26.6.12

## [26.6.11] - 2026-06-17

### 🚀 Features

- Add crawl4ai and stagehand integrations
- Allow custom user data directory in session

### 🐛 Bug Fixes

- Update posthog import path

### 🚜 Refactor

- Remove crawl4ai monkey patches
- [**breaking**] Replace launch_browser with BrowserSession
- Migrate scraping to BrowserSession and Crawl4AiTool
- Replace AsyncWebCrawler with Crawl4AiTool
- Update module paths and fix test mocks
- Replace AsyncWebCrawler with Crawl4AiTool
- Use BrowserSession class for browser handling

### 🧪 Testing

- Add unit tests for integrations
- Remove crawl4ai infrastructure tests
- Refactor end-to-end tests for telemetry
- Update service tests to use Crawl4AiTool
- Update global browser mock to use BrowserSession

### ⚙️ Miscellaneous Tasks

- Remove crawl4ai monkey patching
- Update project metadata and cleanup config
- Remove third_party directory configuration
- Release 26.6.11

## [26.6.10] - 2026-06-17

### 🚀 Features

- Add new agent skills to project

### ⚙️ Miscellaneous Tasks

- Release 26.6.10

## [26.6.9] - 2026-06-15

### 🚀 Features

- Add crawl method to client

### 🐛 Bug Fixes

- Prevent premature closure of shared browser context
- Ignore existing playwright function registration
- Resolve absolute links during validation

### 🧪 Testing

- Add end-to-end tests for scrape and crawl
- Add integration tests for client crawl and scrape

### ⚙️ Miscellaneous Tasks

- Release 26.6.9

## [26.6.8] - 2026-06-15

### 🚀 Features

- Add browser configuration validation

### ⚙️ Miscellaneous Tasks

- Release 26.6.8

## [26.6.7] - 2026-06-15

### 🚀 Features

- Add client configuration settings

### 🚜 Refactor

- [**breaking**] Simplify KodaClient and remove internal scrape logic

### 🧪 Testing

- Add orchestration logic and unit tests for scrape

### ⚙️ Miscellaneous Tasks

- Release 26.6.7

## [26.6.6] - 2026-06-15

### 🚀 Features

- [**breaking**] Add timeout logic and refactor scrape execution

### 🐛 Bug Fixes

- Make timeout optional in page schema

### ⚙️ Miscellaneous Tasks

- Release 26.6.6

## [26.6.5] - 2026-06-15

### 🐛 Bug Fixes

- Make posthog injection conditional

### ⚙️ Miscellaneous Tasks

- Release 26.6.5

## [26.6.4] - 2026-06-15

### 🚀 Features

- Add development dependencies and configuration
- Add windmill and python-logging skills

### 🚜 Refactor

- Replace windmill trace ID with settings
- Simplify sentry trace id tagging

### ⚙️ Miscellaneous Tasks

- Remove lock file
- Update gitignore file
- Resolve version merge conflict
- Release 26.6.4

### Build

- Update lockfiles and exclude third party

## [26.6.3] - 2026-06-13

### ⚙️ Miscellaneous Tasks

- Release 26.6.3

## [26.6.2] - 2026-06-12

### ⚙️ Miscellaneous Tasks

- Release 26.6.2

### Build

- Add windmill submodule

## [26.6.1] - 2026-06-12

### 🚀 Features

- *(koda)* Expose public API in package __init__
- *(koda)* Add Scraper service for page extraction
- *(koda)* Add configuration and model definitions
- *(koda)* Add utility functions for image and text
- *(client)* Implement KodaClient for web scraping
- *(config)* [**breaking**] Add webhook and s3 config support
- *(file)* Add S3 service for file uploads
- *(scrape)* Add S3 upload support for screenshots
- *(koda)* Add webhook service for callbacks
- *(koda)* Export WebhookConfig in package init
- *(koda)* Add S3Config TypedDict for storage
- *(koda)* Add WebhookConfig schema
- *(koda)* Add page extraction and screenshotting service
- *(koda)* Add custom exception classes
- *(client)* Refactor scrape method and add file support
- Add centralized configuration settings
- Add OpenTelemetry logging support
- Update PageAction and ScrapeResponse schemas
- Add session schema and model
- Implement session service for management and MFA
- Add consul lock repository implementation
- Add Redis-based locking repository
- Add IMAP email fetching functionality
- Add JMAP email fetcher
- Add Windmill storage repository
- Add windmill trace context to logger
- Expand settings configuration
- Add browser stealth and analytics infrastructure
- Implement browser service for adapter pattern
- Implement Windmill cache module
- Export file module components
- Implement s3 browser profile persistence
- Add site crawling service and schemas
- Add asynchronous webhook dispatch utility
- Add posthog monolith asset
- Add comprehensive unit and integration tests
- Add crawl script for Windmill
- Add Koda scrape script
- Add cache repository documentation
- Add headless config and legacy browser helper
- Add documentation for raw apps and skills

### 🐛 Bug Fixes

- [**breaking**] Remove provider field from session schema

### 🚜 Refactor

- *(koda)* [**breaking**] Rename ScrapeOptions to ScrapeRequest
- *(s3)* [**breaking**] Decouple file service into standalone functions
- *(webhook)* Convert service class to function
- *(utils)* [**breaking**] Remove unused metadata and HTML tools
- *(koda)* Restructure imports and models
- *(client)* Transition to ScrapeRequest object
- *(tests)* Remove unused html utils tests
- *(koda)* Restructure project structure
- Migrate page service to crawl4ai
- Reorganize page module imports
- [**breaking**] Rewrite KodaClient to decouple from Playwright
- [**breaking**] Convert cache service to class-based structure
- Encapsulate scraping logic into ScrapeJob class
- [**breaking**] Refactor session service into a class
- Encapsulate crawl logic into CrawlJob class
- Refactor service modules to use classes
- Replace logging infrastructure
- [**breaking**] Migrate settings to pydantic-settings
- Replace settings trace_id with Windmill context
- Migrate S3Config to Pydantic model
- [**breaking**] Migrate data structures to pydantic models
- Migrate WebhookConfig to Pydantic
- Update infrastructure module imports and paths

### 📚 Documentation

- Add pull request template
- Add instructions for Windmill AI agent
- Add reference to AGENTS.md

### 🧪 Testing

- *(koda)* Add integration tests for KodaClient
- *(koda)* Add tests for utility functions
- *(koda)* Add unit tests for page extraction logic
- Add unit tests for page service
- Remove obsolete page extraction tests
- Add unit tests for session schema
- Add unit tests for session service
- Remove unified cache repository unit tests

### ⚙️ Miscellaneous Tasks

- Add third-party submodules
- Ignore agent-specific config files
- [**breaking**] Update dependencies and project config
- Drop legacy dependencies and update python
- Update dependency lock file
- Remove third party submodules
- Update logger dependency path
- Update dependencies and add new packages
- Update project release versions
- Configure release-please for monorepo
- Add release-please workflow
- Ignore build and test output files
- Remove claude-specific configuration files
- Remove release-please configuration
- Add automated release workflow
- Configure bumpver and update project version
- Bump version and migrate release workflow
- Release 26.6.1

### Build

- Add comprehensive project documentation standards

<!-- generated by git-cliff -->
