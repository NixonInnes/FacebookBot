import toml
from datetime import datetime
import logging
from logging import handlers

with open('config.toml') as conf_file:
    config = toml.loads(conf_file.read())

log_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s', '%Y-%m-%d %H:%M:%S')
log_handler = handlers.RotatingFileHandler(
    '{logdir}/{today} {file}.log'.format(
        logdir=config['logging']['dir'],
        today=datetime.now().strftime('%Y-%m-%d'),
        file=__name__
    ),
    mode='a',
    maxBytes=250000,
    backupCount=5
)
log_handler.setFormatter(log_formatter)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.addHandler(log_handler)
    try:
        if config['logging'].get(__name__):
            logger.setLevel(config['logging'][__name__]['level'])
        else:
            logger.setLevel(getattr(logging, config['logging']['level']))
    except Exception:
        raise Exception("Incorrectly formatted config file. Unable to assign logging level")
    return logger