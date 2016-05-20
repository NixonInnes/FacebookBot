import os
import argparse
import logging
from FacebookBot import server, log_handler, get_logger

parser = argparse.ArgumentParser(
    description='A facebook messenger bot'
)
parser.add_argument('--host', default='127.0.0.1', help='set server host')
parser.add_argument('--port', default=5000, help='set server port', type=int)
parser.add_argument('--loglevel', default='ERROR', help='set logging level')
parser.add_argument('--logdir', default='logs', help='set log folder destination')
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()


if not os.path.isdir(args.logdir):
    os.makedirs(args.logdir)

if args.debug:
    log_handler.setLevel(logging.DEBUG)
else:
    log_handler.setLevel(getattr(logging, args.loglevel))

logger = get_logger(__name__)

app = server.app

if __name__ == '__main__':
    logger.info('Starting server on {host}:{port}...'.format(host=args.host, port=args.port))
    app.run(host=args.host, port=args.port, debug=args.debug)
