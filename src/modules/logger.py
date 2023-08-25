import sys

from loguru import logger
import os.path
import config


def get_loguru_logger(file_name):
    logger.remove()  # 清除默认配置的处理器和格式器

    logfile = f'{file_name}.log'
    log_path = config.root_path / 'logs' / logfile

    # 添加控制台处理器
    logger.add(sys.stdout, level="DEBUG")
    # 添加文件处理器
    # logger.add(log_path, level="INFO")
    return logger

