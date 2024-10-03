from playwright.async_api import Playwright
from browser_manager.logger import logger


class BrowserManager:
    @staticmethod
    async def init_browser(p: Playwright, headless=False):
        try:
            browser = await p.chromium.launch(
                headless=headless,
                chromium_sandbox=False,
                ignore_default_args=["--enable-automation"],
                channel="chrome",
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-gpu",
                    "--disable-extensions",
                    "--disable-dev-shm-usage",
                    "--disable-setuid-sandbox",
                    "--disable-web-security",
                ],
            )
            return browser
        except Exception as e:
            logger.error(f"浏览器初始化失败: {e}")
            raise
