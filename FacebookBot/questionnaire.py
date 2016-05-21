import toml
import json
from .messenger import Message
from . import get_logger

logger = get_logger(__name__)

with open('questions.toml') as questions_file:
    questions = toml.loads(questions_file.read())

QUESTIONS = questions.get('questions')


class Questionnaire(object):
    def __init__(self, user_id):
        self.user = user_id
        self.complete = False
        self.answers = {q['key']: None for q in QUESTIONS}
        self.current_question_id = 0
        self.expect_input = False

    def get_current_question(self):
        q = QUESTIONS[self.current_question_id]

        if q.get('answers'):
            message = Message()
            self.expect_input = False
            message.add_attachment(
                attachment_type='template',
                template_type='button',
                text=q['question']
            )
            for answer in q.get('answers'):
                message.attachment.payload.add_button(
                    button_type='postback',
                    title=answer,
                    url_or_payload=json.dumps(
                        {
                            'type': 'questionnaire_answer',
                            'data': {
                                'question_key': q['key'],
                                'answer': answer
                            }
                        }
                    )
                )
        else:
            message = Message(text=q['question'])
            self.expect_input = True
        return message

    def set_answer(self, answer, key=None):
        if not key:
            self.answers[QUESTIONS[self.current_question_id]['key']] = answer
        elif key in self.answers:
            self.answers[key] = answer
        else:
            logger.debug('Trying to assign answer to invalid key %s' % key)

    def check_valid_answer(self):
        logger.debug('Checking current answer...')
        logger.debug('Current answer: %s' %
              self.answers[QUESTIONS[self.current_question_id]['key']])
        if self.answers[QUESTIONS[self.current_question_id]['key']] is not None:
            if self.current_question_id is len(QUESTIONS)-1:
                self.complete = True
                return True
            self.current_question_id += 1
            logger.debug('Current answer is valid')
            return True
        logger.debug('Current answer is not valid')
        return False
