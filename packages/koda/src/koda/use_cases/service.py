import asyncio
from typing import Dict, List, Callable, Optional, Awaitable
from playwright.async_api import Page
from koda.use_cases.schema import Action


async def wait_for_networkidle(
    page: Page, wait_for_timeout: int = 1000, timeout_ms: int = 10000
) -> None:
    """Waits for a predefined delay, then safely awaits networkidle load state, catching timeouts."""
    await page.wait_for_timeout(wait_for_timeout)
    try:
        await page.wait_for_load_state("networkidle", timeout=timeout_ms)
    except Exception:
        pass


async def scroll_to(
    page: Page,
    y: Optional[int] = None,
    viewport_height: int = 768,
    wait_callback: Optional[Callable[[], Awaitable[None]]] = None,
) -> None:
    """Scrolls down utilizing PageDown. If y is provided, terminates once window.scrollY >= y.
    If y is None, loops until absolute bottom is reached.
    """
    while True:
        last_scroll_y = await page.evaluate("window.scrollY")
        if y is not None and last_scroll_y >= y:
            break

        await page.keyboard.press("PageDown")

        if wait_callback:
            await wait_callback()
        else:
            await page.wait_for_timeout(100)  # Small fallback wait

        new_scroll_y = await page.evaluate("window.scrollY")
        if new_scroll_y == last_scroll_y:
            break

    await page.evaluate("window.scrollTo(0, 0)")
    await page.wait_for_timeout(1000)


async def screenshot(page: Page, max_height: int = 3072) -> bytes:
    """Calculates exactly document.documentElement.scrollHeight and takes clipped screenshot bounded by max_height."""
    # Bring the page to the front to avoid WSL/Headed Firefox occlusion bugs
    try:
        await page.bring_to_front()
    except Exception:
        pass

    doc_height = await page.evaluate("document.documentElement.scrollHeight")
    capture_height = min(doc_height, max_height)

    # Store original viewport
    original_viewport = page.viewport_size

    # Expand viewport to force Firefox to render the full area in memory
    # This avoids the "static noise" bug caused by using clip + full_page in Firefox Nightly
    await page.set_viewport_size({"width": 1366, "height": capture_height})

    # Small delay for Firefox to paint the expanded viewport
    await page.wait_for_timeout(500)

    shot_bytes = await page.screenshot(full_page=False)

    # Restore original viewport
    if original_viewport:
        await page.set_viewport_size(original_viewport)

    return shot_bytes


async def execute_actions(
    page, actions: List[Action], action_results: Dict[str, list]
) -> None:
    for action in actions:
        try:
            if action.type == "wait":
                if action.milliseconds:
                    await asyncio.sleep(action.milliseconds / 1000.0)
                elif action.selector:
                    kwargs_wait = {}
                    if action.timeout is not None:
                        kwargs_wait["timeout"] = action.timeout
                    await page.wait_for_selector(action.selector, **kwargs_wait)

            elif action.type == "click":
                kwargs_click = {}
                if action.timeout is not None:
                    kwargs_click["timeout"] = action.timeout
                if action.selector:
                    if action.all:
                        elements = await page.query_selector_all(action.selector)
                        for el in elements:
                            await el.click(**kwargs_click)
                    else:
                        await page.click(action.selector, **kwargs_click)

            elif action.type == "write":
                if action.text:
                    await page.keyboard.type(action.text)

            elif action.type == "press":
                if action.key:
                    await page.keyboard.press(action.key)

            elif action.type == "scroll":
                direction = action.direction or "down"
                amount = action.amount or 1000
                if action.selector:
                    await page.evaluate(f"""
                        const el = document.querySelector('{action.selector}');
                        if (el) {{
                            el.scrollBy(0, {amount if direction == "down" else -amount});
                        }}
                    """)
                else:
                    await page.mouse.wheel(
                        0, amount if direction == "down" else -amount
                    )

            elif action.type == "executeJavascript":
                if action.script:
                    result = await page.evaluate(action.script)
                    if "javascriptReturns" in action_results:
                        action_results["javascriptReturns"].append(
                            {"type": str(type(result).__name__), "value": result}
                        )

            elif action.type == "screenshot":
                clip = None
                if (
                    action.viewport
                    and "width" in action.viewport
                    and "height" in action.viewport
                ):
                    clip = {
                        "x": 0,
                        "y": 0,
                        "width": action.viewport["width"],
                        "height": action.viewport["height"],
                    }

                shot_bytes = await page.screenshot(
                    full_page=action.fullPage or False,
                    quality=action.quality,
                    type="jpeg" if action.quality else "png",
                    clip=clip,
                )
                if shot_bytes and "screenshots" in action_results:
                    from oort.file.main import File

                    ext = "jpeg" if action.quality else "png"
                    f = File.from_bytes(
                        shot_bytes, f"screenshot.{ext}", f"image/{ext}"
                    )
                    url = await f.presigned_url  # type: ignore[not-async]
                    action_results["screenshots"].append(url or f.base64)

            elif action.type == "pdf":
                pdf_bytes = await page.pdf(
                    format=action.format or "Letter",
                    landscape=action.landscape or False,
                    scale=action.scale or 1.0,
                )
                if pdf_bytes and "pdfs" in action_results:
                    from oort.file.main import File

                    f = File.from_bytes(
                        pdf_bytes, "document.pdf", "application/pdf"
                    )
                    url = await f.presigned_url  # type: ignore[not-async]
                    action_results["pdfs"].append(url or f.base64)

            elif action.type == "scrape":
                html = await page.content()
                if "scrapes" in action_results:
                    action_results["scrapes"].append({"url": page.url, "html": html})

        except Exception as e:
            print(f"Action {action.type} failed: {str(e)}")
            if "errors" in action_results:
                action_results["errors"].append(
                    {"action": action.type, "error": str(e)}
                )
            if action.ignoreError is False:
                raise
