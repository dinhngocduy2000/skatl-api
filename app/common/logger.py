import logging

formatter = "%(asctime)s - %(levelname)s - %(message)s"


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    ch_format = logging.Formatter(formatter)
    console_handler.setFormatter(ch_format)
    logger.addHandler(console_handler)
    return logger
