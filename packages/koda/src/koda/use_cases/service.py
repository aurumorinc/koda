import asyncio
import base64
from typing import Dict, List, Any
from .schema import Action

async def execute_actions(page, actions: List[Action], action_results: Dict[str, list]) -> None:
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
                            el.scrollBy(0, {amount if direction == 'down' else -amount});
                        }}
                    """)
                else:
                    await page.mouse.wheel(0, amount if direction == 'down' else -amount)
            
            elif action.type == "executeJavascript":
                if action.script:
                    result = await page.evaluate(action.script)
                    if "javascriptReturns" in action_results:
                        action_results["javascriptReturns"].append({
                            "type": str(type(result).__name__),
                            "value": result
                        })
            
            elif action.type == "screenshot":
                clip = None
                if action.viewport and "width" in action.viewport and "height" in action.viewport:
                    clip = {"x": 0, "y": 0, "width": action.viewport["width"], "height": action.viewport["height"]}
                
                shot_bytes = await page.screenshot(
                    full_page=action.fullPage or False,
                    quality=action.quality,
                    type="jpeg" if action.quality else "png",
                    clip=clip
                )
                if shot_bytes and "screenshots" in action_results:
                    b64_shot = base64.b64encode(shot_bytes).decode("utf-8")
                    action_results["screenshots"].append(f"data:image/{'jpeg' if action.quality else 'png'};base64,{b64_shot}")
            
            elif action.type == "pdf":
                pdf_bytes = await page.pdf(
                    format=action.format or "Letter",
                    landscape=action.landscape or False,
                    scale=action.scale or 1.0
                )
                if pdf_bytes and "pdfs" in action_results:
                    b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
                    action_results["pdfs"].append(f"data:application/pdf;base64,{b64_pdf}")
                
            elif action.type == "scrape":
                html = await page.content()
                if "scrapes" in action_results:
                    action_results["scrapes"].append({
                        "url": page.url,
                        "html": html
                    })
                
        except Exception as e:
            print(f"Action {action.type} failed: {str(e)}")
            if "errors" in action_results:
                action_results["errors"].append({
                    "action": action.type,
                    "error": str(e)
                })
            if action.ignoreError is False:
                raise
