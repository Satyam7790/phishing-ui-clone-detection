from pathlib import Path
from backend.config import BROWSER_TIMEOUT, SCREENSHOT_DIRECTORY

def capture_screenshot(url: str, name: str) -> Path | None:
    """Optional passive Playwright capture. Returns None if browser support is absent."""
    try:
        from playwright.sync_api import sync_playwright
        SCREENSHOT_DIRECTORY.mkdir(exist_ok=True)
        path = SCREENSHOT_DIRECTORY / f"{name}.png"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(url, wait_until="domcontentloaded", timeout=BROWSER_TIMEOUT)
            page.screenshot(path=str(path), full_page=False); browser.close()
        return path
    except Exception:
        return None
