import pytest
import sys
import os
import importlib.util
from unittest.mock import MagicMock

class MockWmill:
    @staticmethod
    def get_resource(res):
        if res == "f/koda/default_s3" or res == "test_s3":
            return {
                "endpoint": "http://mock-s3",
                "access_key": "mock_key",
                "secret_key": "mock_secret",
                "bucket": "test-bucket",
                "region": "us-east-1"
            }
        return None

# Globally mock wmill so it works during test collection
sys.modules["wmill"] = MagicMock()
sys.modules["wmill"].get_resource = MockWmill.get_resource

@pytest.fixture(autouse=True)
def clear_browser_env():
    """
    Clear the BROWSER environment variable before any tests are executed,
    so that OS-level variables do not override the defaults during tests.
    """
    os.environ.pop("BROWSER", None)

@pytest.fixture(autouse=True)
def wmill_mock():
    """
    Provide wmill_mock as a fixture for backwards compatibility in tests.
    """
    yield sys.modules["wmill"]

def import_script(relative_path: str, module_name: str):
    """
    Dynamically imports a script from apps/koda-api/f/.
    """
    if module_name in sys.modules:
        return sys.modules[module_name]

    # Assuming tests/ directory is the root of the relative path calculation
    # Current file is apps/koda-api/tests/conftest.py
    tests_dir = os.path.dirname(__file__)
    apps_koda_api_dir = os.path.dirname(tests_dir)
    script_path = os.path.abspath(os.path.join(apps_koda_api_dir, relative_path))
    
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if not spec or not spec.loader:
        raise ImportError(f"Could not load {script_path}")
        
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
