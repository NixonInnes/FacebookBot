import os
import toml
import argparse

with open('config.toml') as conf_file:
    config = toml.loads(conf_file.read())

if not os.path.isdir(config['logging']['dir']):
    os.makedirs(config['logging']['dir'])


from FacebookBot import server, get_logger
from FacebookBot.messenger import Message

parser = argparse.ArgumentParser(
    description='A facebook messenger bot'
)
parser.add_argument('mode', help='runserver|subscribe|setwelcome')
parser.add_argument('--debug', action='store_true', help='start server in debug mode')
args = parser.parse_args()

logger = get_logger(__name__)

app = server.app

if args.mode == 'runserver':
    host = config['server']['host']
    port = config['server']['port']
    ssl_context = (config['server']['ssl_cert_file'], config['server']['ssl_key_file']) if not args.debug else None
    logger.info('Starting server on {host}:{port}{debug}...'.format(
        host=host,
        port=port,
        debug=' in DEBUG mode' if args.debug else ''
    ))
    app.run(
        host=host,
        port=port,
        ssl_context=ssl_context,
        debug=args.debug
    )
elif args.mode == 'subscribe':
    response = server.messenger.subscribe()
    if not response.ok:
        logger.error('Could not subscribe to service. Response: %s' % response.json())
    else:
        logger.info('Successfully subscribed to service.')
elif args.mode == 'setwelcome':
    welcome = Message()
    welcome.add_attachment(
        attachment_type='template',
        template_type='generic',
    )
    welcome.attachment.payload.add_element(
        title=config['facebook']['welcome']['title'],
        subtitle=config['facebook']['welcome'].get('subtitle')
    )
    welcome.attachment.payload.elements[0].add_button(
        button_type='postback',
        title=config['facebook']['welcome']['button_text'],
        url_or_payload='{"type": "start_questionnaire"}'
    )
    response = server.messenger.set_welcome(config['facebook']['page_id'], welcome)
    if not response.ok:
        logger.error('Could not set welcome message. Response: %s' % response.json())
    else:
        logger.info('Successfully updated welcome message.')

else:
    raise