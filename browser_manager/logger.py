import json
import os
from utils.logger import logger

class Logger:
    @staticmethod
    def log_current_active_video(current_active_video):
        log_entry = json.dumps(current_active_video, ensure_ascii=False)
        log_file_path = os.path.join("logs", "comment.log")

        try:
            with open(log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(log_entry + "\n")
            logger.info(f"已将当前视频数据写入日志: {log_entry}")
        except Exception as e:
            logger.error(f"写入日志时出现错误: {e}")
