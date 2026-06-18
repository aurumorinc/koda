import pytest
import asyncio
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import tempfile

class TestServerThread(threading.Thread):
    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        self.server = None
        self.port = None
        self.daemon = True

    def run(self):
        # Capture directory in closure
        directory = self.directory
        
        class Handler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=directory, **kwargs)
                
            def log_message(self, format, *args):
                pass # Suppress logging

        self.server = HTTPServer(('localhost', 0), Handler)
        self.port = self.server.server_port
        self.server.serve_forever()

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()

@pytest.fixture(scope="session")
def local_test_server():
    """Starts a local HTTP server serving static files for E2E tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create index.html
        with open(os.path.join(temp_dir, "index.html"), "w") as f:
            f.write("""
            <html>
            <head><title>Test Index</title></head>
            <body>
                <h1>Welcome to the Test Server</h1>
                <p>This is the main content.</p>
                <a href="/page1.html">Go to Page 1</a>
                <a href="/page2.html">Go to Page 2</a>
                <button id="reveal-btn" onclick="document.getElementById('hidden-text').style.display='block'">Reveal</button>
                <p id="hidden-text" style="display:none;">Hidden Content Revealed!</p>
            </body>
            </html>
            """)
            
        # Create page1.html
        with open(os.path.join(temp_dir, "page1.html"), "w") as f:
            f.write("""
            <html>
            <head><title>Page 1</title></head>
            <body>
                <h1>Page 1</h1>
                <p>Content for page 1.</p>
                <a href="/index.html">Back to Index</a>
            </body>
            </html>
            """)
            
        # Create page2.html
        with open(os.path.join(temp_dir, "page2.html"), "w") as f:
            f.write("""
            <html>
            <head><title>Page 2</title></head>
            <body>
                <h1>Page 2</h1>
                <p>Content for page 2.</p>
                <a href="/index.html">Back to Index</a>
            </body>
            </html>
            """)

        server_thread = TestServerThread(temp_dir)
        server_thread.start()
        
        # Wait for server to start and get port
        import time
        while server_thread.port is None:
            time.sleep(0.1)
            
        base_url = f"http://localhost:{server_thread.port}"
        
        yield base_url
        
        server_thread.stop()
        server_thread.join()

import pytest_asyncio
@pytest_asyncio.fixture(autouse=True)
async def strict_asyncio_exceptions():
    """
    Ensures that any unhandled exception in an asyncio background task 
    fails the pytest suite, mirroring strict production runtimes like Windmill.
    """
    loop = asyncio.get_running_loop()
    original_handler = loop.get_exception_handler()
    
    unhandled_exceptions = []

    def strict_handler(loop, context):
        exc = context.get("exception")
        if not exc:
            future = context.get("future") or context.get("task")
            if future and hasattr(future, "exception") and not future.cancelled():
                try:
                    exc = future.exception()
                except Exception:
                    pass
        
        # We don't fail for TargetClosedError since koda specifically ignores it,
        # but koda's own handler will intercept it first anyway.
        if exc and "TargetClosedError" not in str(type(exc).__name__):
            unhandled_exceptions.append(exc)
            
        if original_handler:
            original_handler(loop, context)
        else:
            loop.default_exception_handler(context)

    loop.set_exception_handler(strict_handler)
    
    yield
    
    # Restore original and assert no unhandled exceptions occurred
    loop.set_exception_handler(original_handler)
    
    if unhandled_exceptions:
        pytest.fail(f"Unhandled asyncio exceptions occurred during test: {unhandled_exceptions}")
