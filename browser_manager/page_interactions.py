import asyncio
import random
from browser_manager.logger import logger


class PageInteractions:
    @staticmethod
    async def browse_video(page):
        wait_time_before_action = random.uniform(2, 12)
        logger.info(f"等待 {wait_time_before_action:.2f} 秒，准备浏览下一个视频")
        await asyncio.sleep(wait_time_before_action)

        logger.info("按下 ↓ 键切换到下一个视频")
        await page.keyboard.press("ArrowDown")

        logger.info("获取视频标题和ID")
        await asyncio.sleep(1)

    @staticmethod
    async def get_video_id(page):
        try:
            video_element = page.locator(
                '[data-e2e="feed-item"]>[data-e2e="feed-active-video"]'
            )
            video_id = await video_element.get_attribute("data-e2e-vid")
            logger.info(f"当前视频ID: {video_id}")
            return f"https://www.douyin.com/video/{video_id}"
        except Exception as e:
            logger.error(f"获取视频ID时出现错误: {e}")
            return None

    @staticmethod
    async def jump_to_modal(page):
        await asyncio.sleep(3)
        await page.wait_for_selector('.JLxgOO5G div:has-text("多列")', timeout=35000)
        await page.locator('.JLxgOO5G div:has-text("多列")').click()
        await page.wait_for_selector(".NA7vT_tM .AMqhOzPC", timeout=35000)
        logger.info(".AMqhOzPC 元素已找到")

        elements = await page.locator(".NA7vT_tM .AMqhOzPC").all()

        if len(elements) >= 3:
            await elements[2].click()
            logger.info("成功点击第三个 .AMqhOzPC 元素")
            await asyncio.sleep(3)
            await page.keyboard.press("ArrowDown")

            await asyncio.sleep(2)
            await PageInteractions.click_second_video_comment_icon(page)
        else:
            logger.warning(".AMqhOzPC 元素少于三个，无法点击第三个")

    @staticmethod
    async def click_second_video_comment_icon(page):
        try:
            await page.wait_for_selector(
                '[data-e2e="feed-active-video"]', timeout=35000
            )
            logger.info('[data-e2e="feed-active-video"] 元素已找到')

            active_videos = await page.locator('[data-e2e="feed-active-video"]').all()

            if len(active_videos) >= 2:
                comment_icon = active_videos[1].locator(
                    '[data-e2e="feed-comment-icon"]'
                )
                await comment_icon.click()
                logger.info("成功点击第二个视频的评论图标")
            else:
                logger.warning(
                    "[data-e2e='feed-active-video'] 元素少于两个，无法点击第二个视频的评论图标，点第一个"
                )
                comment_icon = active_videos[0].locator(
                    '[data-e2e="feed-comment-icon"]'
                )
                await comment_icon.click()

        except Exception as e:
            logger.error(f"发生错误: {str(e)}")
