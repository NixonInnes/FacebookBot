import requests, json
from . import get_logger

logger = get_logger(__name__)

API_URL = "https://graph.facebook.com/v2.6/me/messages"


class Messenger(object):

    def __init__(self, token):
        self.access_token = token

    def send(self, recipient_id, message):
        headers = {'Content-Type': 'application/json'}
        params = {'access_token': self.access_token}
        data = {
            'recipient': {'id': recipient_id},
            'message': {'text': message}
        }

        response = requests.post(API_URL, headers=headers, params=params, json=data)
        logger.debug('Response OK: %s' % response.ok)
        logger.debug('Response: %s' % response.json)
        #if not response.ok:
            # log error
            #pass

        return response.json()

    def send_q(self, recipient_id, question, answers):
        headers = {'Content-Type': 'application/json'}
        params = {'access_token': self.access_token}
        data = {
            'recipient': {'id': recipient_id},
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'button',
                        'text': question,
                    }
                }
            },
        }

        buttons = []
        for answer in answers:
            buttons.append({'type': 'postback', 'title': answer[0], 'payload': json.dumps(answer[1])})

        data['message']['attachment']['payload']['buttons'] = buttons

        response = requests.post(API_URL, headers=headers, params=params, json=data)
        logger.debug('Response OK: %s' % response.ok)
        logger.debug('Response: %s' % response.json())
        # if not response.ok:
        # log error
        # pass

        return response.json()

