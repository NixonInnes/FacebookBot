from datetime import datetime
import logging
from logging import handlers

log_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s', '%Y-%m-%d %H:%M:%S')
log_handler = handlers.RotatingFileHandler(
    '{logdir}/{today} {file}.log'.format(logdir='logs', today=datetime.now().strftime('%Y-%m-%d'), file='server'),
    mode='a',
    maxBytes=250000,
    backupCount=5
)
log_handler.setFormatter(log_formatter)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.addHandler(log_handler)
    logger.setLevel(logging.NOTSET)
    return logger