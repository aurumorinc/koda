import os
import json
import time
import logging
from typing import Optional
import httpx
from opentelemetry import trace
from playwright.async_api import Page, Request, Response, BrowserContext
from koda.config.main import settings

logger = logging.getLogger("koda.posthog")

def _get_otel_trace_id() -> str:
    """Extracts the current OTel trace ID."""
    # 1. Try active span
    span = trace.get_current_span()
    if span and span.get_span_context().is_valid:
        return format(span.get_span_context().trace_id, "032x")
    
    # 2. Fallback to Windmill context
    from python_logging.integrations.windmill import get_windmill_context
    return get_windmill_context().get("trace_id", "")

async def handle_playwright_request(url: str, method: str, data: str, content_type: Optional[str] = None) -> dict:
    """Proxy transport for posthog-js running in the browser."""
    print(f"handle_playwright_request called with url={url}")
    async with httpx.AsyncClient() as client:
        try:
            headers = {}
            if content_type:
                headers['Content-Type'] = content_type
                
            if method.upper() == "GET":
                resp = await client.get(url, headers=headers)
            else:
                resp = await client.post(url, headers=headers, content=data)
            return {"status": resp.status_code, "body": resp.text}
        except Exception as e:
            logger.error(f"PostHog proxy transport error: {e}")
            return {"status": 500, "body": str(e)}

async def setup_playwright_transport(context: BrowserContext) -> None:
    """Expose the Python transport function to the browser context."""
    print(f"setup_playwright_transport called, handle_playwright_request is {handle_playwright_request}")
    await context.expose_function("__playwright_posthog_send", handle_playwright_request)

async def setup_network_capture(page: Page, posthog_api_key: str) -> None:
    """Intercept network requests out-of-band and relay them to posthog-js."""
    async def on_request_finished(request: Request):
        try:
            url = request.url
            if posthog_api_key in url or "/__koda/" in url or "/s/" in url or "/e/" in url or "/i/" in url:
                return

            resource_type = request.resource_type
            if resource_type not in ("fetch", "xhr"):
                return

            method = request.method
            request_headers = request.headers
            
            request_body = request.post_data if request.post_data else None

            response = await request.response()
            if not response:
                return

            status = response.status
            response_headers = response.headers

            response_body = None
            content_type = response_headers.get("content-type", "").lower()
            if any(t in content_type for t in ("json", "text", "javascript", "xml")):
                try:
                    response_body = await response.text()
                except Exception:
                    pass

            timing = request.timing
            start_time_ms = timing.get("startTime")
            if start_time_ms is None:
                start_time_ms = time.time() * 1000
            start_time_ms = int(start_time_ms)
            
            response_end = timing.get("responseEnd", -1)
            end_time_ms = start_time_ms + int(response_end) if response_end != -1 else start_time_ms

            response_start = timing.get("responseStart", -1)
            time_to_first_byte = int(response_start) if response_start != -1 else 0

            network_data = {
                "url": url,
                "method": method,
                "requestHeaders": request_headers,
                "requestBody": request_body,
                "responseHeaders": response_headers,
                "responseBody": response_body,
                "status": status,
                "startTime": start_time_ms,
                "endTime": end_time_ms,
                "timeToFirstByte": time_to_first_byte,
            }

            await page.evaluate(
                """data => {
                    if (window.__posthog_playwright_network_receiver) {
                        const timeOrigin = Math.floor(Date.now() - performance.now());
                        const relativeStart = Math.max(0, data.startTime - timeOrigin);
                        const relativeEnd = Math.max(relativeStart, data.endTime - timeOrigin);
                        
                        const formattedData = {
                            requests: [{
                                name: data.url,
                                method: data.method,
                                requestHeaders: data.requestHeaders,
                                requestBody: data.requestBody,
                                responseHeaders: data.responseHeaders,
                                responseBody: data.responseBody,
                                status: data.status,
                                startTime: Math.round(relativeStart),
                                endTime: Math.round(relativeEnd),
                                timeOrigin: timeOrigin,
                                timestamp: data.startTime,
                                initiatorType: 'playwright'
                            }]
                        };
                        window.__posthog_playwright_network_receiver(formattedData);
                    }
                }""",
                network_data
            )
        except Exception as e:
            logger.debug(f"Error in network capture finished handler: {e}")

    async def on_request_failed(request: Request):
        try:
            url = request.url
            if posthog_api_key in url or "/__koda/" in url or "/s/" in url or "/e/" in url or "/i/" in url:
                return

            resource_type = request.resource_type
            if resource_type not in ("fetch", "xhr"):
                return

            method = request.method
            request_headers = request.headers
            
            request_body = request.post_data if request.post_data else None

            timing = request.timing
            start_time_ms = timing.get("startTime")
            if start_time_ms is None:
                start_time_ms = time.time() * 1000
            start_time_ms = int(start_time_ms)

            network_data = {
                "url": url,
                "method": method,
                "requestHeaders": request_headers,
                "requestBody": request_body,
                "responseHeaders": {},
                "responseBody": f"Request failed: {request.failure}",
                "status": 0,
                "startTime": start_time_ms,
                "endTime": start_time_ms,
                "timeToFirstByte": 0,
            }

            await page.evaluate(
                """data => {
                    if (window.__posthog_playwright_network_receiver) {
                        const timeOrigin = Math.floor(Date.now() - performance.now());
                        const relativeStart = Math.max(0, data.startTime - timeOrigin);
                        const relativeEnd = Math.max(relativeStart, data.endTime - timeOrigin);
                        
                        const formattedData = {
                            requests: [{
                                name: data.url,
                                method: data.method,
                                requestHeaders: data.requestHeaders,
                                requestBody: data.requestBody,
                                responseHeaders: data.responseHeaders,
                                responseBody: data.responseBody,
                                status: data.status,
                                startTime: Math.round(relativeStart),
                                endTime: Math.round(relativeEnd),
                                timeOrigin: timeOrigin,
                                timestamp: data.startTime,
                                initiatorType: 'playwright'
                            }]
                        };
                        window.__posthog_playwright_network_receiver(formattedData);
                    }
                }""",
                network_data
            )
        except Exception as e:
            logger.debug(f"Error in network capture failed handler: {e}")

    page.on("requestfinished", on_request_finished)
    page.on("requestfailed", on_request_failed)

async def inject_posthog_monolith(page: Page, api_key: str, host: str) -> None:
    """Inject the WeakMap-based posthog-monolith.js into the page."""
    monolith_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "posthog-monolith.js")
    if not os.path.exists(monolith_path):
        logger.error(f"PostHog monolith not found at {monolith_path}")
        return

    with open(monolith_path, "r") as f:
        monolith_js = f.read()

    trace_id = _get_otel_trace_id()

    injection_script = f"""
    try {{
        if (window.top === window && window.location.href !== 'about:blank') {{
            console.log("Injecting PostHog monolith...");
            {monolith_js}
            globalThis.posthog.init('{api_key}', {{
                api_host: '{host}',
                autocapture: true,
                capture_pageview: true,
                persistence: 'localStorage',
                disable_session_recording: false,
                disable_compression: true,
                api_transport: function(options) {{
                    console.log("PostHog transport called with url: " + options.url);
                    if (window.__playwright_posthog_send) {{
                        window.__playwright_posthog_send(
                            options.url, 
                            options.method || 'POST', 
                            typeof options.data === 'string' ? options.data : JSON.stringify(options.data), 
                            options.headers ? options.headers['Content-Type'] : null
                        );
                    }}
                }},
                session_recording: {{
                    minimumDurationMilliseconds: 0,
                    recordHeaders: true,
                    recordBody: true,
                    networkPayloadCapture: {{
                        recordHeaders: true,
                        recordBody: true
                    }}
                }},
                __extensionClasses: globalThis.posthog.__defaultExtensionClasses,
                loaded: function(ph) {{
                    console.log("PostHog loaded!");
                    if ('{trace_id}') {{
                        ph.register({{ "$trace_id": "{trace_id}" }});
                    }}
                }}
            }});
            globalThis.posthog.startSessionRecording();
            console.log("PostHog initialized!");
        }}
    }} catch (e) {{
        console.error("PostHog Injection Error: " + e.message);
    }}
    """
    await page.add_init_script(injection_script)
