import pytest
import inspect
from pydantic import BaseModel
import sys
from unittest.mock import MagicMock
import koda # triggers patching
from koda.client import KodaClient

class TitleSchema(BaseModel):
    title: str

@pytest.mark.asyncio
async def test_stagehand_integration(local_test_server):
    """Test that Stagehand can successfully use a BrowserSession to extract elements via KodaClient."""
    # Mock stagehand since it's an optional dependency and might not be installed
    mock_stagehand = MagicMock()
    
    async def mock_init(*args, **kwargs):
        pass
    async def mock_close(*args, **kwargs):
        pass
        
    class StagehandMock:
        def __init__(self, **kwargs):
            self.client = kwargs.get("client")
        async def init(self, *args, **kwargs):
            pass
        async def close(self, *args, **kwargs):
            pass

    mock_stagehand.Stagehand = StagehandMock
    sys.modules['stagehand'] = mock_stagehand
    
    # re-trigger patch manually for mock
    from koda.integrations.stagehand import KodaStagehand
    mock_stagehand.Stagehand = KodaStagehand

    try:
        koda_client_instance = KodaClient()
        stagehand = KodaStagehand(client=koda_client_instance)
        
        await stagehand.init()
        assert stagehand.page is not None
        assert stagehand.context is not None
        
        await stagehand.page.goto(f"{local_test_server}/index.html")
        assert "index.html" in stagehand.page.url
        
        await stagehand.close()
    finally:
        if 'stagehand' in sys.modules:
            del sys.modules['stagehand']
