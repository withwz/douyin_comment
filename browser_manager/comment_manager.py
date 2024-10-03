from utils.config import get_random_caption
from browser_manager.logger import logger
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


class CommentManager:
    @staticmethod
    def get_random_comment(comments_list):
        return get_random_caption(comments_list)

    @staticmethod
    async def post_comment(page, comment):
        logger.info("尝试点击评论输入框")
        try:
            await page.wait_for_selector(
                ".comment-input-inner-container .d66pgCnu", timeout=35000
            )
            logger.info("评论输入框已找到")
            comment_input = page.locator(".comment-input-inner-container .d66pgCnu")
            await comment_input.click()
        except PlaywrightTimeoutError:
            logger.warning("评论输入框未找到，点击弹出元素")
            return

        logger.info("输入评论文本")
        await page.wait_for_timeout(500)
        await comment_input.type(comment)

        logger.info("发布评论")
        await page.wait_for_timeout(500)
        await page.locator(".commentInput-right-ct .oXIqR6qH").click()
