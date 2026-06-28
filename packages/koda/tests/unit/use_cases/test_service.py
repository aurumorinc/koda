import pytest
from unittest.mock import AsyncMock, patch
from koda.use_cases.schema import Action
from koda.use_cases.service import execute_actions

@pytest.mark.asyncio
async def test_execute_actions_wait():
    page_mock = AsyncMock()
    actions = [Action(type="wait", milliseconds=100)]
    results = {}
    await execute_actions(page_mock, actions, results)
    # wait with ms doesn't call page methods, just asyncio.sleep
    assert not page_mock.wait_for_selector.called

@pytest.mark.asyncio
async def test_execute_actions_click():
    page_mock = AsyncMock()
    actions = [Action(type="click", selector=".btn")]
    results = {}
    await execute_actions(page_mock, actions, results)
    page_mock.click.assert_called_once_with(".btn")

@pytest.mark.asyncio
async def test_execute_actions_javascript():
    page_mock = AsyncMock()
    page_mock.evaluate.return_value = "hello"
    actions = [Action(type="executeJavascript", script="return 'hello';")]
    results = {"javascriptReturns": []}
    await execute_actions(page_mock, actions, results)
    page_mock.evaluate.assert_called_once_with("return 'hello';")
    assert results["javascriptReturns"] == [{"type": "str", "value": "hello"}]

@pytest.mark.asyncio
async def test_execute_actions_error_handling():
    page_mock = AsyncMock()
    page_mock.click.side_effect = Exception("Click failed")
    actions = [Action(type="click", selector=".btn", ignoreError=True)]
    results = {"errors": []}
    
    # Should not raise exception
    await execute_actions(page_mock, actions, results)
    assert len(results["errors"]) == 1
    assert results["errors"][0]["action"] == "click"
    
    # Should raise exception
    actions_fail = [Action(type="click", selector=".btn", ignoreError=False)]
    with pytest.raises(Exception, match="Click failed"):
        await execute_actions(page_mock, actions_fail, results)
