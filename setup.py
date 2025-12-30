import logging
from filters import MDCFilter

import logging
from logging.handlers import RotatingFileHandler
import os

import socket
container_id = socket.gethostname()
from appLogger import normal_app_logger
normLogger = normal_app_logger()

MAX_LOG_SIZE = os.environ.get("MAX_LOG_SIZE")
BACKUP_COUNT = os.environ.get("BACKUP_COUNT")

MAX_LOG_SIZE = (1 * 1024 * 1024) if MAX_LOG_SIZE==None else (int(MAX_LOG_SIZE) * 1024 * 1024)
BACKUP_COUNT = 1 if BACKUP_COUNT==None else int(BACKUP_COUNT)

normLogger.info("MAX LOG SIZE : {}".format(MAX_LOG_SIZE))
normLogger.info("BACKUP COUNT : {}".format(BACKUP_COUNT))


def setup_logger(component):
    logger = logging.getLogger(component)
    logger.setLevel(logging.INFO)

    log_path = f"logs/{component}.{container_id}.log"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    handler = RotatingFileHandler(
        log_path,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-5s %(process)d --- "
        "[%(threadName)s] %(name)s "
        "[traceId=%(traceId)s spanId=%(spanId)s "
        "paymentId=%(paymentId)s] : "
        "%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S.%f"
    )

    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    logger.propagate = False
    return logger

