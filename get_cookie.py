import asyncio
import os
from playwright.async_api import Playwright, async_playwright


class creator_douyin:
    def __init__(self, phone, timeout: int = 120):
        """
        初始化
        :param phone: 手机号
        :param timeout: 你要等待多久，单位秒
        """
        self.timeout = timeout * 1000
        self.phone = phone
        self.path = os.path.abspath("")
        self.desc = "cookie_%s.json" % phone

        if not os.path.exists(os.path.join(self.path, "cookie")):
            os.makedirs(os.path.join(self.path, "cookie"))

    async def __cookie(self, playwright: Playwright) -> None:
        browser = await playwright.chromium.launch(channel="chrome", headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # 反检测自动化脚本，避免页面检测 WebDriver
        await page.add_init_script(path="stealth.min.js")

        # 打开抖音主页
        await page.goto("https://www.douyin.com/?recommend=1")

        # 等待一些时间以确保页面加载
        await page.wait_for_timeout(2000)  # 等待2秒

        # 等待Modal弹窗加载
        await page.wait_for_selector(".login-mask-enter-done", timeout=self.timeout)

        # 等待并点击验证码登录的 Tab
        try:
            # print(await page.content())
            # 显式等待验证码登录 tab 的 img 元素加载完成，最大等待时间为 `timeout`
            await page.wait_for_selector(
                '[aria-label="验证码登录"]', timeout=self.timeout
            )
            await page.locator('[aria-label="验证码登录"]').click()

            print("成功点击验证码登录 tab")
        except Exception as e:
            print(f"点击验证码登录 tab 失败: {e}")

        # 填入手机号
        await page.locator(".web-login-normal-input__input").fill(self.phone)

        # 发送验证码
        try:
            await page.wait_for_selector(
                'span:has-text("获取验证码")', timeout=self.timeout
            )
            await page.locator('span:has-text("获取验证码")').click()
            print("成功点击获取验证码按钮")
        except Exception as e:
            print(f"点击获取验证码按钮失败: {e}")

        try:
            # 等待登录成功
            try:
                # 等待直到弹窗关闭
                await page.wait_for_selector(
                    ".login-mask-enter-done", state="hidden", timeout=self.timeout
                )
                print("登录弹窗已关闭")
            except Exception as e:
                print(f"等待弹窗关闭时发生错误: {e}")

            # 获取 Cookie 并保存
            cookies = await context.cookies()
            cookie_txt = ""
            for i in cookies:
                cookie_txt += i.get("name") + "=" + i.get("value") + "; "
            try:
                # 检查 sessionid 是否存在，确认登录成功
                cookie_txt.index("sessionid")
                print(self.phone + " ——> 登录成功")
                await context.storage_state(
                    path=os.path.join(self.path, "cookie", self.desc)
                )
            except ValueError:
                print(self.phone + " ——> 登录失败，本次操作不保存cookie")
        except Exception as e:
            print(self.phone + " ——> 登录失败，本次操作不保存cookie", e)
        finally:
            await page.close()
            await context.close()
            await browser.close()

    async def main(self):
        async with async_playwright() as playwright:
            await self.__cookie(playwright)


def main():
    phone = "14751799042"
    app = creator_douyin(phone, 60)
    asyncio.run(app.main())


main()
