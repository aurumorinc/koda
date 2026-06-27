import pytest
from aiohttp import web
from koda.modules.browser.service import BrowserSession

async def start_local_server(port=8081):
    async def handle_strict_csp(request):
        # Serve an HTML page with a strict CSP that blocks all inline scripts
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>CSP Test</title>
        </head>
        <body>
            <h1>CSP is active</h1>
            <script>window.secret = 'csp-blocked';</script>
        </body>
        </html>
        """
        headers = {
            "Content-Security-Policy": "default-src 'self'; script-src 'none';"
        }
        return web.Response(text=html, content_type="text/html", headers=headers)

    app = web.Application()
    app.router.add_get('/', handle_strict_csp)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', port)
    await site.start()
    return runner

@pytest.mark.asyncio
async def test_csp_bypass_via_network_interception():
    # Start the test server
    runner = await start_local_server(port=8081)
    
    try:
        # Launch browser session (this should automatically inject the CSP stripping route)
        async with BrowserSession() as context:
            page = await context.new_page()
            
            # Navigate to the strict CSP page
            response = await page.goto("http://localhost:8081/")
            
            # The inline script should have been executed if CSP was stripped.
            # But wait, our CSP stripping removes the header, so the inline script SHOULD run.
            # However, Playwright `evaluate` is the main thing we want to test.
            
            # Attempt to evaluate a script. If CSP was active, eval might be blocked.
            eval_result = await page.evaluate("1 + 1")
            assert eval_result == 2, "evaluate should succeed when CSP is stripped"
            
            # Check if inline script ran (if CSP was stripped, script-src 'none' is gone)
            secret = await page.evaluate("window.secret")
            assert secret == "csp-blocked", "Inline script should have executed because CSP was stripped"
            
            # Ensure the actual response headers seen by Playwright don't contain CSP
            assert response is not None
            headers = response.headers
            assert "content-security-policy" not in headers
            
    finally:
        await runner.cleanup()
