import asyncio
import os
import random
import json
import traceback
from utils.logger import logger
from utils.config import get_random_caption, goto_page
from playwright.async_api import Playwright, async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


class DouyinCommenter:
    def __init__(self, cookie_file: str):
        self.cookie_file = cookie_file
        self.ua = {
            "web": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36",
        }
        self.current_active_video = {"url": "", "comment": ""}
        self.no_more = False

    async def init_browser(self, p: Playwright, headless=False):
        """初始化Playwright浏览器"""
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

    async def check_login_status(self, page):
        """检查是否登录"""
        logger.info("正在判断账号是否登录")
        try:
            element = await page.query_selector("#RkbQLUok")
            if element:
                logger.info("未登录状态，存在 id='RkbQLUok'")
                return False
            else:
                logger.info("已登录状态，不存在 id='RkbQLUok'")
                return True
        except Exception as e:
            logger.error(f"登录检查时出现错误: {e}")
            return False

    async def browse_video(self, page):
        """浏览视频，按下 ↓ 键以切换到下一个视频"""
        # 随机生成等待时间，范围在2到12秒之间
        wait_time_before_action = random.uniform(2, 12)
        logger.info(f"等待 {wait_time_before_action:.2f} 秒，准备浏览下一个视频")
        await asyncio.sleep(wait_time_before_action)

        # 按下 ↓ 键切换到下一个视频
        logger.info("按下 ↓ 键切换到下一个视频")
        await page.keyboard.press("ArrowDown")

        logger.info("获取视频标题和ID")
        await asyncio.sleep(1)

        # 获取视频ID并写入日志
        await self.get_video_id(page)

    async def get_video_id(self, page):
        """获取当前活跃视频的ID"""
        try:
            # 定位到 data-e2e="feed-active-video" 的元素
            video_element = page.locator('[data-e2e="feed-active-video"]')
            # 获取该元素上的 data-e2e-vid 属性值
            video_id = await video_element.get_attribute("data-e2e-vid")
            logger.info(f"当前视频ID: {video_id}")
            new_url = f"https://www.douyin.com/video/{video_id}"
            if new_url == self.current_active_video["url"]:
                logger.info("没有更多了")
                self.no_more = True
            else:
                self.no_more = False
            self.current_active_video["url"] = new_url
        except Exception as e:
            logger.error(f"获取视频ID时出现错误: {e}")
            return None

    async def post_comment(self, page, comments_made):
        """发布评论"""
        # 再次生成随机时间，确保行为的自然性
        wait_time_after_action = random.uniform(2, 5)
        logger.info(f"等待 {wait_time_after_action:.2f} 秒后开始评论")
        await asyncio.sleep(wait_time_after_action)

        logger.info("尝试点击评论输入框")

        try:
            # 首先尝试等待并点击评论输入框
            await page.wait_for_selector(
                ".comment-input-inner-container .d66pgCnu", timeout=35000
            )
            logger.info("评论输入框已找到")

            # 定位并点击评论输入框
            comment_input = page.locator(".comment-input-inner-container .d66pgCnu")
            await comment_input.click()

        except PlaywrightTimeoutError:
            logger.warning("评论输入框未找到，点击弹出元素")

            # 如果评论输入框未出现，点击弹出框
            await self.click_second_video_comment_icon(page)
            return

        # 输入评论
        logger.info("输入评论文本")
        await page.wait_for_timeout(500)
        random_caption = get_random_caption()
        self.current_active_video["comment"] = random_caption
        await comment_input.type(random_caption)

        # # 图片添加
        # assets_folder = os.path.join(os.getcwd(), "assets")
        # # 获取 assets 文件夹下的所有文件路径
        # file_list = [
        #     os.path.join(assets_folder, file)
        #     for file in os.listdir(assets_folder)
        #     if os.path.isfile(os.path.join(assets_folder, file))
        # ]
        # # 从文件列表中随机选择一个文件
        # file_path = random.choice(file_list)
        # if file_path is not None:
        #     await page.set_input_files("input[type='file']", file_path)

        # 发布评论
        logger.info("发布评论")
        await page.wait_for_timeout(500)
        await page.locator(".commentInput-right-ct .oXIqR6qH").click()

        # 记录评论内容
        comments_made.append(random_caption)
        logger.info(
            f"已发布评论: {random_caption}，当前累计评论数: {len(comments_made)}"
        )

    def log_current_active_video(self):
        """将当前视频的URL和评论写入logs/comment.log文件"""
        log_entry = json.dumps(self.current_active_video, ensure_ascii=False)
        log_file_path = os.path.join("logs", "comment.log")

        try:
            with open(log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(log_entry + "\n")
            logger.info(f"已将当前视频数据写入日志: {log_entry}")
        except Exception as e:
            logger.error(f"写入日志时出现错误: {e}")

    async def simulate_browsing(self, page):
        """模拟浏览器行为，浏览视频和偶尔评论"""
        logger.info("开始模拟浏览器行为")
        comments_made = []  # 用于存储已发布的评论

        try:
            while True:

                # 没有更多了跳转到起始页面，重新点击进入
                if self.no_more:
                    await page.goto(goto_page)
                    await self.jump_to_modal(page)

                # 浏览视频
                await self.browse_video(page)

                # 随机决定是否评论，1到3之间的随机数，2/3 的几率
                if random.randint(1, 3) <= 2:
                    logger.info("决定发表评论")
                    if not self.no_more:
                        await self.post_comment(page, comments_made)
                    else:
                        logger.info("没有更多了")
                else:
                    logger.info("决定继续浏览，不发表评论")
                    self.current_active_video["comment"] = "不发表评论"
                    await asyncio.sleep(random.uniform(5, 10))  # 停留一段时间后继续浏览

                # 视频链接和评论内容写入log
                self.log_current_active_video()

        except Exception as e:
            traceback.print_exc()
            logger.error(f"模拟浏览器行为时出现错误: {e}")

    async def jump_to_modal(self, page):
        await asyncio.sleep(3)
        # 选择多列
        await page.wait_for_selector('.JLxgOO5G div:has-text("多列")', timeout=35000)
        await page.locator('.JLxgOO5G div:has-text("多列")').click()
        # 等待 .AMqhOzPC 元素的出现
        await page.wait_for_selector(".NA7vT_tM .AMqhOzPC", timeout=35000)
        logger.info(".AMqhOzPC 元素已找到")

        # 获取所有 .AMqhOzPC 元素
        elements = await page.locator(".NA7vT_tM .AMqhOzPC").all()

        print("len(elements): ", len(elements))
        if len(elements) >= 3:
            # 点击第三个元素
            await elements[2].click()
            logger.info("成功点击第三个 .AMqhOzPC 元素")
            await asyncio.sleep(3)  # 停留一段时间后按↓跳过提示遮罩层
            await page.keyboard.press("ArrowDown")

            await asyncio.sleep(2)  # 停留一段时间后点击打开评论区
            await self.click_second_video_comment_icon(page)
        else:
            logger.warning(".AMqhOzPC 元素少于三个，无法点击第三个")

    async def click_second_video_comment_icon(self, page):
        """
        点击第二个 [data-e2e="feed-active-video"] 下的 [data-e2e="feed-comment-icon"]。
        :param page: Playwright页面对象
        """
        try:
            # 等待所有 [data-e2e="feed-active-video"] 元素的出现
            await page.wait_for_selector(
                '[data-e2e="feed-active-video"]', timeout=35000
            )
            logger.info('[data-e2e="feed-active-video"] 元素已找到')

            # 获取所有 [data-e2e="feed-active-video"] 元素
            active_videos = await page.locator('[data-e2e="feed-active-video"]').all()

            print("len(active_videos): ", len(active_videos))
            if len(active_videos) >= 2:
                # 定位到第二个 [data-e2e="feed-active-video"] 下的 [data-e2e="feed-comment-icon"]
                comment_icon = active_videos[1].locator(
                    '[data-e2e="feed-comment-icon"]'
                )

                # 点击评论图标
                await comment_icon.click()
                logger.info("成功点击第二个视频的评论图标")
            else:
                logger.warning(
                    "[data-e2e='feed-active-video'] 元素少于两个，无法点击第二个视频的评论图标，点第一个"
                )
                comment_icon = active_videos[0].locator(
                    '[data-e2e="feed-comment-icon"]'
                )

                # 点击评论图标
                await comment_icon.click()

        except Exception as e:
            logger.error(f"发生错误: {str(e)}")

    async def start_browsing(self, p: Playwright) -> None:
        """启动浏览评论的主要流程"""
        browser = await self.init_browser(p)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},  # 屏幕大小
            storage_state=self.cookie_file,
            user_agent=self.ua["web"],
        )
        page = await context.new_page()

        try:
            await page.add_init_script(path="stealth.min.js")
            await page.goto(goto_page)
            is_logged_in = await self.check_login_status(page)

            if is_logged_in:
                await self.jump_to_modal(page)
                await self.simulate_browsing(page)
            else:
                logger.error("请检查登录状态，未登录无法继续")

        except Exception as e:
            logger.error(f"浏览过程中发生错误: {e}")
        finally:
            await context.close()
            await browser.close()

    async def main(self):
        """主入口函数"""
        async with async_playwright() as playwright:
            await self.start_browsing(playwright)


def find_files(directory, extension):
    """在指定路径中查找指定类型的文件"""
    path = os.path.abspath(directory)
    if not os.path.exists(path):
        os.makedirs(path)

    return [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
        if file.endswith(extension)
    ]


async def run():
    """程序运行入口"""
    cookie_files = find_files("cookie", ".json")

    if cookie_files:
        commenter = DouyinCommenter(cookie_files[0])
        await commenter.main()
    else:
        logger.error("未找到任何cookie文件")


if __name__ == "__main__":
    # 运行主异步函数
    asyncio.run(run())
