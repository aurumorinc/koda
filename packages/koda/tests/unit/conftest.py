import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def mock_launch_browser():
    """
    Globally mock BrowserSession for all unit tests.
    Unit tests should NEVER launch a real browser. This ensures tests run fast
    and physically cannot leak browser processes.
    """
    with patch("koda.modules.browser.service.BrowserSession", new_callable=MagicMock) as mock_launch:
        mock_browser = MagicMock()
        mock_launch.return_value.__aenter__.return_value = mock_browser
        yield mock_launch
