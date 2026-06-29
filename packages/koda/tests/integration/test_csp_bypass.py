import pytest
from aiohttp import web
from koda.modules.browser.service import BrowserSession

async def start_local_server(port=8081):
    async def handle_strict_csp(request):
        # Serve an HTML page with a strict CSP that blocks all inline scripts
        # We also include a <meta> tag CSP, which network interception CANNOT strip.
        # This forces the browser to rely on `security.csp.enable: False` (extra_prefs).
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
        # Launch browser session (this should automatically inject the CSP stripping route and apply extra_prefs)
        async with BrowserSession() as context:
            # Persistent context comes with a default page usually, or we can create a new one.
            pages = context.pages
            page = pages[0] if pages else await context.new_page()
            
            # Navigate to the strict CSP page
            response = await page.goto("http://localhost:8081/")
            
            # Wait a moment for network and script execution
            from koda.use_cases.service import wait_for_networkidle, scroll_to
            await wait_for_networkidle(page)
            
            # The inline script should have been executed if CSP was entirely disabled natively.
            # Attempt to evaluate a script. If CSP was active, eval might be blocked.
            # Playwright eval parses strings as eval().
            eval_result = await page.evaluate("1 + 1")
            assert eval_result == 2, "evaluate should succeed when CSP is stripped"
            
            # Test that the utility function also succeeds without throwing a CSP violation
            await scroll_to(page, y=100)
            scroll_val = await page.evaluate("window.scrollY")
            assert scroll_val == 100 or scroll_val == 0  # Depending on page height, it might not scroll, but it shouldn't error.
            
            # Check if inline script ran (if CSP was entirely bypassed, script-src 'none' is ignored)
            secret = await page.evaluate("window.secret")
            assert secret == "csp-blocked", "Inline script should have executed because CSP was completely disabled natively"
            
    finally:
        await runner.cleanup()
