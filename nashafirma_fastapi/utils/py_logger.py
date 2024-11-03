import logging


def get_logger(name):
    _format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s - "
    file = "nf_logs.log"

    file_handler = logging.FileHandler(file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(_format))

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(_format))

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
