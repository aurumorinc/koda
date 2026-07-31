import pytest
from unittest.mock import AsyncMock
from koda.modules.page.schema import Action
from koda.modules.page.service import execute_actions, wait_for_networkidle, scroll_to, screenshot


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





@pytest.mark.asyncio
async def test_wait_for_networkidle_success():
    page_mock = AsyncMock()
    await wait_for_networkidle(page_mock, wait_for_timeout=10, timeout_ms=100)
    page_mock.wait_for_timeout.assert_called_once_with(10)
    page_mock.wait_for_load_state.assert_called_once_with("networkidle", timeout=100)


@pytest.mark.asyncio
async def test_wait_for_networkidle_timeout_silenced():
    page_mock = AsyncMock()
    page_mock.wait_for_load_state.side_effect = Exception("Timeout")
    # Should not raise exception
    await wait_for_networkidle(page_mock, wait_for_timeout=10, timeout_ms=100)
    page_mock.wait_for_load_state.assert_called_once_with("networkidle", timeout=100)


@pytest.mark.asyncio
async def test_scroll_to_infinite_end():
    page_mock = AsyncMock()
    # Mock window.scrollY evaluation
    # Returns 0, then 1000, then 1000 (meaning it stopped scrolling)
    page_mock.evaluate.side_effect = [0, 1000, 1000, 1000, None]

    await scroll_to(page_mock, y=None)

    # 2 loops = 2 PageDowns, plus the final scrollTo(0,0)
    assert page_mock.keyboard.press.call_count == 2
    page_mock.keyboard.press.assert_called_with("PageDown")


@pytest.mark.asyncio
async def test_scroll_to_specific_y():
    page_mock = AsyncMock()
    # Scroll to y=1500.
    # Evaluate sequence: 0, 1000, 2000
    page_mock.evaluate.side_effect = [0, 1000, 2000, None]

    await scroll_to(page_mock, y=1500)

    # 1 loop
    assert page_mock.keyboard.press.call_count == 1


@pytest.mark.asyncio
async def test_screenshot():
    page_mock = AsyncMock()
    page_mock.evaluate.return_value = 5000  # doc height
    page_mock.screenshot.return_value = b"image_data"

    res = await screenshot(page_mock, max_height=3072)

    assert res == b"image_data"
    page_mock.screenshot.assert_called_once_with(
        full_page=False
    )
