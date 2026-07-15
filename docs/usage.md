# Koda API Usage Documentation

Koda is a web scraping and extraction engine exposed via Windmill API endpoints. Because scraping tasks are long-running, endpoints trigger asynchronous jobs. 

Tools like **Postman**, **Insomnia**, or **n8n** can import the cURL requests provided below. To get the final result, you submit the job (which returns a Job ID), and then poll the Windmill result endpoint until the job is complete.

---

## The Asynchronous Execution Flow

For all endpoints, you will follow a similar flow to retrieve data:

1. **Submit the Job:** Send a `POST` request to the endpoint URL. You will receive a Job ID (`UUID`) as raw text in the response body.
2. **Poll for Result:** Send a `GET` request to the Windmill result endpoint (`/api/w/aurumor/jobs_u/completed/get_result_maybe/<UUID>`) using the UUID you received.
3. **Check Status:** Evaluate the JSON response. If `"completed": true`, the data is available in the `"result"` key. If it is `false`, wait a few seconds and try again.

---

## Common Objects

### Webhook Object (Input)
When provided, Koda will dispatch POST requests to your URL on job lifecycle events (`started`, `completed`, `failed`).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | string | **Required** | The destination URL to receive POST payloads. |
| `headers` | dict | `null` | Key-value pairs for HTTP headers (e.g. `{"Authorization": "Bearer..."}`). |
| `metadata` | dict | `null` | Custom data to echo back in every webhook payload. |
| `events` | list[string] | `["started", "completed", "failed"]` | Events to subscribe to. |

### Webhook Response Payload (Output)
When Koda dispatches a webhook to your server, the POST body will conform to the following schema.

**Example `completed` event:**
```json
{
  "success": true,
  "type": "completed",
  "id": "abc12345-6789-defg-hijk-lmnopqrs",
  "webhookId": "f7d3a8e9-...",
  "data": {
    "url": "https://example.com",
    "markdown": "# Example Domain\n\nThis domain is for use in illustrative examples..."
  },
  "error": null,
  "metadata": {
    "job_name": "example-scrape",
    "user_id": "123"
  }
}
```

**Example `failed` event:**
```json
{
  "success": false,
  "type": "failed",
  "id": "abc12345-6789-defg-hijk-lmnopqrs",
  "webhookId": "e6c2b7d8-...",
  "data": [],
  "error": "TimeoutError: Page failed to load within 60000ms",
  "metadata": {
    "job_name": "example-scrape",
    "user_id": "123"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | `true` if the job completed successfully, `false` otherwise. |
| `type` | string | The event type (e.g., `started`, `completed`, `failed`). |
| `id` | string | The Windmill Job ID (UUID) returned from your initial POST request. |
| `webhookId` | string | Unique UUID for this specific webhook delivery. |
| `data` | any | The extracted output (JSON array/object) on success. Empty for `started`/`failed`. |
| `error` | string | Error message string if the job failed. `null` otherwise. |
| `metadata` | dict | Echoed directly from the `metadata` you passed in the initial webhook request. |

### Action Object
Simulate browser interactions before extraction.

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | **Required.** Action type: `click`, `wait`, `scroll`, `screenshot`, `script`, `type`, etc. |
| `selector` | string | CSS/XPath selector for interaction. |
| `value` | any | Value to type or input. |
| `milliseconds`| int | Time to wait in milliseconds. |
| `text` | string | Text value for assertions or input. |
| `key` | string | Keyboard key to press (e.g., `Enter`). |
| `script` | string | JavaScript code to execute. |
| `direction` | string | Scroll direction (`up`, `down`, `left`, `right`). |
| `amount` | int | Scroll amount in pixels. |
| `all` | bool | Whether to target all matching elements. |
| `fullPage` | bool | Screenshot the entire page. |
| `quality` | int | Screenshot quality (0-100). |
| `viewport` | dict | `{"width": int, "height": int}` |
| `format` | string | Image format (e.g. `png`, `jpeg`). |
| `landscape` | bool | Orientation for printing/screenshots. |
| `scale` | float | Scale factor. |
| `timeout` | int | Interaction timeout in ms. |
| `ignoreError`| bool | Ignore action failures (Default: `true`). |

---

## 1. Scrape Single URL
Extracts structured data from a single webpage.

**Endpoint:** `POST https://windmill.aurumor.com/api/w/aurumor/jobs/run/p/f/koda/scrape`

### Request Payload

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | string | **Required** | The URL to scrape. |
| `formats` | list[string] | `["markdown"]` | Desired output formats (`markdown`, `screenshot`, `html`, `links`, `images`). |
| `onlyMainContent`| bool | `true` | Attempt to extract only the core article/content. |
| `actions` | list[Action] | `[]` | List of browser actions to execute before extraction. |
| `timeout` | int | `60000` | Hard timeout in milliseconds. |
| `webhook` | object | `null` | Webhook configuration object. |

### cURL Example: Submit Job
*(Fully populated payload - formatted as a single line for easy import into Postman/n8n)*
```bash
curl -X POST "https://windmill.aurumor.com/api/w/aurumor/jobs/run/p/f/koda/scrape" -H "Authorization: Bearer YOUR_WINDMILL_TOKEN" -H "Content-Type: application/json" -d '{"url":"https://example.com","formats":["markdown","screenshot","html","links","images"],"onlyMainContent":true,"timeout":60000,"actions":[{"type":"click","selector":"#accept-cookies","milliseconds":1000,"timeout":5000,"ignoreError":true},{"type":"wait","milliseconds":2000}],"webhook":{"url":"https://webhook.site/your-uuid","headers":{"Authorization":"Bearer webhook-secret"},"metadata":{"job_name":"example-scrape","user_id":"123"},"events":["started","completed","failed"]}}'
```

### cURL Example: Poll for Result
```bash
curl -X GET "https://windmill.aurumor.com/api/w/aurumor/jobs_u/completed/get_result_maybe/YOUR_JOB_UUID" -H "Authorization: Bearer YOUR_WINDMILL_TOKEN"
```

---

## 2. Batch Scrape
Extracts data from multiple URLs concurrently.

**Endpoint:** `POST https://windmill.aurumor.com/api/w/aurumor/jobs/run/p/f/koda/batch_scrape`

### Request Payload

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `urls` | list[string] | `[]` | List of URLs to scrape with default parameters. |
| `requests` | list[object]| `[]` | List of `ScrapeRequest` objects for URL-specific parameter overrides. |
| `formats` | list[string] | `["markdown"]` | Global output formats. |
| `onlyMainContent`| bool | `true` | Global content extraction preference. |
| `actions` | list[Action] | `[]` | Global browser actions applied to all URLs. |
| `timeout` | int | `60000` | Global timeout in ms. |
| `webhook` | object | `null` | Global webhook configuration object. |
| `maxConcurrency` | int | `10` | Maximum number of concurrent scrapers. |
| `ignoreInvalidURLs`| bool | `true` | If true, skips malformed URLs instead of failing the batch. |

### cURL Example: Submit Job
*(Fully populated payload - formatted as a single line for easy import into Postman/n8n)*
```bash
curl -X POST "https://windmill.aurumor.com/api/w/aurumor/jobs/run/p/f/koda/batch_scrape" -H "Authorization: Bearer YOUR_WINDMILL_TOKEN" -H "Content-Type: application/json" -d '{"urls":["https://example.com/1","https://example.com/2"],"requests":[{"url":"https://example.com/3","formats":["screenshot"],"onlyMainContent":false,"timeout":120000,"actions":[{"type":"scroll","direction":"down","amount":500,"ignoreError":true}],"webhook":{"url":"https://webhook.site/override-uuid","headers":{"X-Custom":"override"},"metadata":{"type":"specific-request-webhook"},"events":["completed","failed"]}}],"formats":["markdown","screenshot","links"],"onlyMainContent":true,"actions":[{"type":"wait","milliseconds":1000}],"timeout":60000,"maxConcurrency":5,"ignoreInvalidURLs":true,"webhook":{"url":"https://webhook.site/your-uuid","headers":{"Authorization":"Bearer webhook-secret"},"metadata":{"job_name":"batch-scrape","batch_id":"ABC-123"},"events":["started","completed","failed"]}}'
```

### cURL Example: Poll for Result
```bash
curl -X GET "https://windmill.aurumor.com/api/w/aurumor/jobs_u/completed/get_result_maybe/YOUR_JOB_UUID" -H "Authorization: Bearer YOUR_WINDMILL_TOKEN"
```

---

## 3. Crawl Domain
Traverses a website starting from a seed URL to discover and optionally extract data from multiple pages.

**Endpoint:** `POST https://windmill.aurumor.com/api/w/aurumor/jobs/run/p/f/koda/crawl`

### Request Payload

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | string | **Required** | The seed URL to start crawling. |
| `prompt` | string | `null` | LLM extraction prompt applied to crawled pages. |
| `excludePaths` | list[string] | `null` | Glob patterns or exact paths to exclude. |
| `includePaths` | list[string] | `null` | Glob patterns or exact paths to exclusively include. |
| `maxDiscoveryDepth`| int | `0` | Max depth from seed URL (0 = unlimited). |
| `sitemap` | string | `"include"` | `"include"`, `"ignore"`, or `"only"`. |
| `ignoreQueryParameters`| bool| `false` | Treat URLs with different query params as identical. |
| `regexOnFullURL` | bool | `false` | Apply path inclusions/exclusions using Regex instead of Glob. |
| `limit` | int | `10000` | Max number of pages to process. |
| `crawlEntireDomain`| bool | `false` | Allow crawling subpaths above the seed path. |
| `allowExternalLinks`| bool | `false` | Allow crawling cross-origin domain links. |
| `allowSubdomains` | bool | `false` | Allow crawling sibling subdomains. |
| `ignoreRobotsTxt` | bool | `false` | Bypass `robots.txt` rules. |
| `robotsUserAgent` | string | `null` | Impersonate this user agent when reading `robots.txt`. |
| `delay` | float | `null` | Fixed delay (in seconds) between requests to respect rate limits. |
| `maxConcurrency` | int | `10` | Max concurrent pages being crawled. |
| `webhook` | object | `null` | Webhook configuration object. |
| `zeroDataRetention`| bool | `false` | If true, rely entirely on webhooks and do not persist results to Windmill output. |
| `scrapeOptions` | object | *(See below)* | Configuration rules for extracting data from individual pages. |

**ScrapeOptions Object (`scrapeOptions`)**
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `formats` | list[string] | `["markdown"]` | `markdown`, `screenshot`, `html`, `links`. |
| `onlyMainContent`| bool | `true` | Try to extract only core content. |
| `onlyCleanContent`| bool | `false` | Remove navigation/footer elements aggressively. |
| `includeTags` | list[string] | `null` | Specific HTML tags/selectors to retain. |
| `excludeTags` | list[string] | `null` | Specific HTML tags/selectors to strip. |
| `maxAge` | int | `172800000` | Max cache age (48 hours in ms). |
| `minAge` | int | `null` | Min cache age. |
| `headers` | dict | `null` | Custom HTTP headers injected into requests. |
| `waitFor` | int | `0` | Wait time (ms) before starting extraction on each page. |
| `mobile` | bool | `false` | Emulate a mobile device viewport. |
| `skipTlsVerification`| bool | `true` | Ignore invalid SSL certificates. |
| `timeout` | int | `60000` | Page timeout (ms, max 300,000). |
| `parsers` | list | `["pdf"]` | Parsers to enable. |
| `actions` | list[Action] | `null` | Actions to run on every crawled page. |
| `location`| dict | `null` | Geolocation override. |
| `removeBase64Images`| bool| `true` | Strip inline base64 images from output. |
| `blockAds`| bool | `true` | Enable ad-blocker network intercepts. |
| `proxy` | string | `"auto"` | Proxy setting or rotation logic. |
| `storeInCache` | bool | `true` | Save results in the caching layer. |
| `lockdown`| bool | `false` | Disable extraneous JS features for safety. |
| `profile` | dict | `null` | Browser profile configurations. |

### cURL Example: Submit Job
*(Fully populated payload - formatted as a single line for easy import into Postman/n8n)*
```bash
curl -X POST "https://windmill.aurumor.com/api/w/aurumor/jobs/run/p/f/koda/crawl" -H "Authorization: Bearer YOUR_WINDMILL_TOKEN" -H "Content-Type: application/json" -d '{"url":"https://docs.example.com","prompt":"Extract the main pricing points and product names.","excludePaths":["/login*","/admin/*"],"includePaths":["/blog/*","/docs/*"],"maxDiscoveryDepth":3,"sitemap":"include","ignoreQueryParameters":false,"regexOnFullURL":false,"limit":10000,"crawlEntireDomain":false,"allowExternalLinks":false,"allowSubdomains":false,"ignoreRobotsTxt":false,"robotsUserAgent":"KodaBot","delay":1.5,"maxConcurrency":10,"zeroDataRetention":false,"scrapeOptions":{"formats":["markdown","screenshot","html","links","images"],"onlyMainContent":true,"onlyCleanContent":false,"includeTags":["article","main","h1"],"excludeTags":["nav","footer","aside"],"maxAge":172800000,"minAge":0,"headers":{"X-Custom-Header":"value"},"waitFor":1000,"mobile":false,"skipTlsVerification":true,"timeout":60000,"parsers":["pdf","docx"],"actions":[{"type":"scroll","direction":"down","amount":1000,"timeout":2000,"ignoreError":true}],"location":{"latitude":40.7128,"longitude":-74.0060},"removeBase64Images":true,"blockAds":true,"proxy":"auto","storeInCache":true,"lockdown":false,"profile":{"name":"default"}},"webhook":{"url":"https://webhook.site/your-uuid","headers":{"Authorization":"Bearer webhook-secret"},"metadata":{"job_name":"example-crawl","tenant_id":"ABC"},"events":["started","completed","failed"]}}'
```

### cURL Example: Poll for Result
```bash
curl -X GET "https://windmill.aurumor.com/api/w/aurumor/jobs_u/completed/get_result_maybe/YOUR_JOB_UUID" -H "Authorization: Bearer YOUR_WINDMILL_TOKEN"
```

---

## 4. YouTube Profile Scout
Specialized orchestration endpoint to bypass protections, extract YouTube channel handles, and perform deep multi-tab profile scrapes.

**Endpoint:** `POST https://windmill.aurumor.com/api/w/aurumor/jobs/run/p/f/koda/scouts/scrape_youtube_profile`

### Request Payload

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | string | **Required** | The YouTube profile/channel URL. |
| `formats` | list[string] | `["screenshot"]` | Extraction formats (screenshots are returned as S3 presigned URLs if configured, otherwise Base64). |
| `timeout` | int | `600000` | Job timeout in ms (10 minutes default). |
| `max_concurrency` | int | `1` | Max concurrent orchestrations. |
| `webhook` | object | `null` | Webhook configuration object. |

### cURL Example: Submit Job
*(Fully populated payload - formatted as a single line for easy import into Postman/n8n)*
```bash
curl -X POST "https://windmill.aurumor.com/api/w/aurumor/jobs/run/p/f/koda/scouts/scrape_youtube_profile" -H "Authorization: Bearer YOUR_WINDMILL_TOKEN" -H "Content-Type: application/json" -d '{"url":"https://www.youtube.com/@mkbhd","formats":["screenshot","markdown"],"timeout":600000,"max_concurrency":2,"webhook":{"url":"https://webhook.site/your-uuid","headers":{"Authorization":"Bearer webhook-secret"},"metadata":{"job_name":"youtube-scout","platform":"youtube"},"events":["started","completed","failed"]}}'
```

### cURL Example: Poll for Result
```bash
curl -X GET "https://windmill.aurumor.com/api/w/aurumor/jobs_u/completed/get_result_maybe/YOUR_JOB_UUID" -H "Authorization: Bearer YOUR_WINDMILL_TOKEN"
