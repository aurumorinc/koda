import pytest
from worldline import structlog
import psutil
import os

logger = structlog.get_logger(__name__)

def get_child_processes():
    """Get a list of all child processes (node, firefox) spawned by this test runner."""
    current_process = psutil.Process(os.getpid())
    children = current_process.children(recursive=True)
    return [p for p in children if p.name() in ("node", "firefox", "firefox-bin")]

@pytest.fixture(autouse=True)
def monitor_process_leaks(request):
    """Monitor each test for leaked child processes."""
    before_children = get_child_processes()
    
    yield
    
    after_children = get_child_processes()
    
    # Find any new children that were spawned during the test and not killed
    new_children = [p for p in after_children if p not in before_children]
    
    if new_children:
        # Log the leak
        logger.error(f"Test {request.node.name} leaked {len(new_children)} processes: {new_children}")
        
        # Forcefully kill the leaked processes so they don't crash the server
        for p in new_children:
            try:
                p.kill()
            except psutil.NoSuchProcess:
                pass
                
        # Fail the test explicitly
        pytest.fail(f"Test leaked {len(new_children)} processes (node/firefox).")

def pytest_sessionfinish(session, exitstatus):
    """Nuclear cleanup: forcefully kill any remaining node/firefox processes spawned by this session."""
    children = get_child_processes()
    if children:
        print(f"\n[Nuclear Cleanup] Found {len(children)} orphaned processes. Terminating...")
        for p in children:
            try:
                p.kill()
            except psutil.NoSuchProcess:
                pass
import pytest
import asyncio
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
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
        if exc and "TargetClosedError" not in str(type(exc).__name__) and "TimeoutError" not in str(type(exc).__name__):
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
