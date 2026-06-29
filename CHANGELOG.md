# Changelog v0.10.7

## Fixes

* **YouTube Scraping Timeout**
  Increased the default request timeout for YouTube scraping operations to 600,000ms to prevent premature connection termination during long-running requests.
  (Commit: [c06eb30](https://github.com/aurumorinc/koda/commit/c06eb30a))

## Performance

* **S3 Multipart Upload Threshold**
  Increased the multipart upload threshold to 500MB to resolve `SignatureDoesNotMatch` errors occurring during large file transfers.
  (Commits: [284121e](https://github.com/aurumorinc/koda/commit/284121ea), [309cb51](https://github.com/aurumorinc/koda/commit/309cb516))
