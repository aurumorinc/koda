import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from koda.integrations.stagehand import StagehandTool

@pytest.mark.asyncio
@patch("koda.integrations.stagehand.Stagehand")
async def test_stagehand_tool_extract(mock_stagehand_cls):
    mock_stagehand = AsyncMock()
    mock_stagehand_cls.return_value = mock_stagehand
    
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_context.new_page.return_value = mock_page
    
    tool = StagehandTool()
    request = {
        "action": "extract",
        "instruction": "Get the title"
    }
    
    await tool.execute(mock_context, request)
    
    mock_context.new_page.assert_called_once()
    mock_stagehand_cls.assert_called_once_with(page=mock_page)
    mock_stagehand.extract.assert_called_once_with("Get the title")
    mock_page.close.assert_called_once()

@pytest.mark.asyncio
@patch("koda.integrations.stagehand.Stagehand")
async def test_stagehand_tool_act(mock_stagehand_cls):
    mock_stagehand = AsyncMock()
    mock_stagehand_cls.return_value = mock_stagehand
    
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_context.new_page.return_value = mock_page
    
    tool = StagehandTool()
    request = {
        "action": "act",
        "instruction": "Click the button"
    }
    
    await tool.execute(mock_context, request)
    
    mock_stagehand.act.assert_called_once_with("Click the button")

@pytest.mark.asyncio
@patch("koda.integrations.stagehand.Stagehand")
async def test_stagehand_tool_observe(mock_stagehand_cls):
    mock_stagehand = AsyncMock()
    mock_stagehand_cls.return_value = mock_stagehand
    
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_context.new_page.return_value = mock_page
    
    tool = StagehandTool()
    request = {
        "action": "observe",
        "instruction": "Find all links"
    }
    
    await tool.execute(mock_context, request)
    
    mock_stagehand.observe.assert_called_once_with("Find all links")
