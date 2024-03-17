import logging


def setup_global_logger():
    log_format = "[%(asctime)s] - [%(levelname)s] : %(message)s"
    date_format = "%H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
