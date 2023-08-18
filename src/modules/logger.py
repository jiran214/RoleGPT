import logging
import os.path

import config


def get_logger(file_name):
    logger = logging.getLogger(file_name)
    logger.setLevel(level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    if config.debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level=logging.DEBUG)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    else:
        filename = os.path.join(config.root_path / f'logs/{file_name}.log')
        file_handler = logging.FileHandler(filename)
        # file_handler = handlers.TimedRotatingFileHandler(filename=f'{file_name}.log', when='D')
        file_handler.setLevel(level=logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger