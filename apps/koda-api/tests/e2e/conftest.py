import pytest
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
