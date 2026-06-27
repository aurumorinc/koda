import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from koda.integrations.stagehand import StagehandTool, KodaStagehand

def test_stagehand_module_patching():
    try:
        import stagehand
        assert stagehand.Stagehand is KodaStagehand
    except ImportError:
        pass

@pytest.mark.asyncio
@patch("koda.modules.browser.service.BrowserSession")
async def test_koda_stagehand_lifecycle(mock_browser_session_cls):
    mock_session = AsyncMock()
    mock_browser_session_cls.return_value = mock_session
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_context.new_page.return_value = mock_page
    mock_session.__aenter__.return_value = mock_context
    
    mock_client = MagicMock()
    stagehand_instance = KodaStagehand(client=mock_client)
    
    # KodaStagehand subclass of BaseStagehand (which might be object if not installed)
    # So we only test if we can call init/close and they trigger our mocked session
    if hasattr(stagehand_instance, "init"):
        # We don't patch BaseStagehand.init because it doesn't exist natively.
        # We just call init and verify Koda behavior.
        with patch("koda.integrations.stagehand.BaseStagehand.close", create=True, new_callable=AsyncMock) as mock_super_close:
            await stagehand_instance.init()
            
            assert stagehand_instance._koda_session == mock_session
            mock_session.__aenter__.assert_called_once()
            mock_context.new_page.assert_called_once()
            
            await stagehand_instance.close()
            mock_session.__aexit__.assert_called_once()
            assert stagehand_instance._koda_session is None

@pytest.mark.asyncio
async def test_stagehand_tool_extract():
    mock_stagehand = AsyncMock()
    mock_stagehand_cls = MagicMock(return_value=mock_stagehand)
    
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_context.new_page.return_value = mock_page
    
    tool = StagehandTool()
    request = {
        "action": "extract",
        "instruction": "Get the title"
    }
    
    import sys
    mock_module = MagicMock()
    mock_module.Stagehand = mock_stagehand_cls
    with patch.dict(sys.modules, {"stagehand": mock_module}):
        await tool.execute(mock_context, request)
    
    mock_context.new_page.assert_called_once()
    mock_stagehand_cls.assert_called_once_with(page=mock_page)
    mock_stagehand.extract.assert_called_once_with("Get the title")
    mock_page.close.assert_called_once()

@pytest.mark.asyncio
async def test_stagehand_tool_act():
    mock_stagehand = AsyncMock()
    mock_stagehand_cls = MagicMock(return_value=mock_stagehand)
    
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_context.new_page.return_value = mock_page
    
    tool = StagehandTool()
    request = {
        "action": "act",
        "instruction": "Click the button"
    }
    
    import sys
    mock_module = MagicMock()
    mock_module.Stagehand = mock_stagehand_cls
    with patch.dict(sys.modules, {"stagehand": mock_module}):
        await tool.execute(mock_context, request)
    
    mock_stagehand.act.assert_called_once_with("Click the button")

@pytest.mark.asyncio
async def test_stagehand_tool_observe():
    mock_stagehand = AsyncMock()
    mock_stagehand_cls = MagicMock(return_value=mock_stagehand)
    
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_context.new_page.return_value = mock_page
    
    tool = StagehandTool()
    request = {
        "action": "observe",
        "instruction": "Find all links"
    }
    
    import sys
    mock_module = MagicMock()
    mock_module.Stagehand = mock_stagehand_cls
    with patch.dict(sys.modules, {"stagehand": mock_module}):
        await tool.execute(mock_context, request)
    
    mock_stagehand.observe.assert_called_once_with("Find all links")
