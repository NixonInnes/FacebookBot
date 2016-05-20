from flask import Flask, request
import os, json
from .messenger import Messenger
from .questionnaire import Questionnaire
from . import get_logger

logger = get_logger(__name__)

VERIFY_TOKEN = os.getenv('MESSENGER_VERIFY_TOKEN', 'TEST_TOKEN_09345h349534985h3894h5398h')
FACEBOOK_TOKEN = os.getenv('FACEBOOK_TOKEN', 'EAAH9MS2hZCtYBAJKiWzoZBinOo6BtLqJ193KWw6zkQZAeH3dMhLGBB0PXVy7gMoZAbk8KZCowlBzEHnpZB4mhspx99NdR7Ts3QIDrpZCuE7rJhVZAaQzvWWlEu6JQ2ZBO9JSZAgtogGkCNo4px2eo1mAPP1Aoa1zjFOSmSm7s0ndkZBAly6dn7oob6o')

app = Flask(__name__)
messenger = Messenger(FACEBOOK_TOKEN)

questionnaires = {}


@app.route("/webhook/7ce461549aaaac965a753cb7abcd0807ca845087a053a007b5", methods=['GET', 'POST'])
def bot():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        if token == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return 'Bad Token'

    if request.method == 'POST':
        post = request.json
        events = post['entry'][0]['messaging']
        for event in events:
            logger.debug(event)
            sender = event['sender'].get('id')
            if sender not in questionnaires:
                q = Questionnaire(sender)
                questionnaires[sender] = q
                logger.debug('Added new questionnaire')
            else:
                logger.debug('Selecting existing questionnaire')
                q = questionnaires.get(sender)

            logger.debug('Current question: %s\nAnswers: %s' % q.get_current_question())

            if event.get('postback'):
                logger.debug('Received postback')
                payload = event['postback'].get('payload')
                logger.debug('Payload: %s' % payload)
                payload = json.loads(payload)
                q.set_answer(payload[0], payload[1])
                q.check_valid_answer()

            if event.get('message'):
                logger.debug('Received message')
                message = event['message'].get('text')
                logger.debug('Message: %s' % message)
                if q.get_current_question()[1] is None:
                    q.set_current_answer(message)
                    q.check_valid_answer()

            if q.get_current_question()[1] is None:
                logger.debug('Sending message')
                messenger.send(sender, q.get_current_question()[0])
            else:
                logger.debug('Sending buttons')
                messenger.send_q(sender, q.get_current_question()[0], q.get_current_question()[1])
        return '', 200


if __name__ == '__main__':
    ssl_context = ('certs/fullchain.pem', 'certs/privkey.pem')
    app.run(host='0.0.0.0', port=5000, ssl_context=ssl_context)
