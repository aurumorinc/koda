import pytest
import logging
import psutil
import os

logger = logging.getLogger(__name__)

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
