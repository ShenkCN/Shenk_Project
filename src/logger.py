import logging
import os
from logging.handlers import TimedRotatingFileHandler

def get_logger(name: str) -> logging.Logger:
    """
    获取一个带有控制台输出和文件切割功能的 logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 防止重复添加 handler
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 1. 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 2. 文件输出（按天切割）
        # 确保 logs 目录存在
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = TimedRotatingFileHandler(
            filename=os.path.join(log_dir, 'runtime.log'),
            when='midnight',  # 每天午夜切割
            interval=1,
            backupCount=7,    # 保留最近 7 天的日志
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger