from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1366, "height": 768})
    page = context.new_page()
    page.goto("https://www.youtube.com/@mkbhd")

    def _wait_for_network():
        page.wait_for_timeout(1000)
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass

    # To capture the FULL dialog without scroll truncation, expand the viewport so the dialog scales up naturally
    page.set_viewport_size({"width": 1366, "height": 3072})
    page.get_by_role("button").filter(has_text="...more").click()
    dialog = page.locator("tp-yt-paper-dialog").first
    dialog.wait_for(state="visible")
    _wait_for_network()
    dialog.screenshot(path="about_dialog.png")
    # Revert viewport back
    page.set_viewport_size({"width": 1366, "height": 768})

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
