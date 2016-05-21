from flask import Flask, request
import os, json
from .messenger import Messenger, Message
from .questionnaire import Questionnaire
from . import get_logger

logger = get_logger(__name__)

WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')
if not WEBHOOK_VERIFY_TOKEN:
    logger.error('WEBHOOK_VERIFY_TOKEN is not defined in the environment variables.')
WEBHOOK_URL_EXTENSION = os.getenv('WEBHOOK_URL_EXTENSION')
if not WEBHOOK_URL_EXTENSION:
    logger.error('WEBHOOK_URL_EXTENSION is not defined in the environment variables.')
FACEBOOK_PAGE_TOKEN = os.getenv('FACEBOOK_PAGE_TOKEN')
if not FACEBOOK_PAGE_TOKEN:
    logger.error('FACEBOOK_PAGE_TOKEN is not defined in the environment variables.')

app = Flask(__name__)
messenger = Messenger(FACEBOOK_PAGE_TOKEN)

questionnaires = {}
complete_questionnaires = []


@app.route("/webhook/"+WEBHOOK_URL_EXTENSION, methods=['GET', 'POST'])
def bot():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        if token == WEBHOOK_VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return 'Bad Token'

    if request.method == 'POST':
        post = request.json
        events = post['entry'][0]['messaging']
        for event in events:
            logger.debug(event)
            sender = event['sender'].get('id')

            payload = json.loads(event['postback'].get('payload')) if event.get('postback') else None
            message = event['message'].get('text') if event.get('message') else None

            if sender in questionnaires:
                q = questionnaires[sender]
                if payload:
                    if payload.get('type') == 'questionnaire_answer':
                        q.set_answer(payload['data']['answer'], key=payload['data']['question_key'])
                        q.check_valid_answer()

                elif message:
                    if q.expect_input:
                        q.set_answer(message)
                        q.check_valid_answer()

                if q.complete:
                    messenger.send(sender, Message(text='The questionnare is complete!'))
                    complete_questionnaires.append(
                        {
                            'user': sender,
                            'answers': q.answers
                        }
                    )
                    questionnaires.pop(sender)
                else:
                    messenger.send(sender, q.get_current_question())

            else:
                if payload:
                    if payload.get('type') == 'start_questionnaire':
                        q = Questionnaire(sender)
                        questionnaires[sender] = q
                        logger.debug('Added new questionnaire')
                        messenger.send(sender, q.get_current_question())

        return 'success', 200
