import logging
from . import get_logger

logger = get_logger(__name__)

QUESTIONS = [
    {
        'id': 'address',
        'question': 'What is the address of the property?'
    },
    {
        'id': 'output',
        'question': 'What is the desired output?',
        'answers': [
            'Images & Video',
            'Maps & Data'
        ]
    },
    {
        'id': 'property_type',
        'question': 'What is the property type?',
        'answers': [
            'Construction Site or Farm',
            'Public Building',
            'Other'
        ]
    },
    {
        'id': 'permission',
        'question': 'Do you have permission to survey the area?',
        'answers': [
            'Yes, I am the owner',
            'Yes, I have permission from the owner',
            'No'
        ]
    },
    {
        'id': 'when',
        'question': 'When is the data required?'
    },
    {
        'id': 'description',
        'question': 'Please briefly describe the goals of the survey.'
    }
]


class Questionnaire(object):
    def __init__(self, user_id):
        self.user = user_id
        self.answers = {q['id']: None for q in QUESTIONS}
        self.current_question_id = 0

    def get_current_question(self):
        q = QUESTIONS[self.current_question_id]
        if q.get('answers'):
            return q['question'], [(a, (q['id'], a)) for a in q['answers']]
        return q['question'], None

    def set_current_answer(self, answer):
        self.answers[QUESTIONS[self.current_question_id]['id']] = answer

    def set_answer(self, key, answer):
        if key in self.answers:
            self.answers[key] = answer
        else:
            logger.debug('Trying to assign answer to invalid key %s' % key)

    def check_valid_answer(self):
        logger.debug('Checking current answer...')
        logger.debug('Current answer: %s' %
              self.answers[QUESTIONS[self.current_question_id]['id']])
        if self.answers[QUESTIONS[self.current_question_id]['id']] is not None:
            self.current_question_id += 1
            logger.debug('Current answer is valid')
            return True
        logger.debug('Current answer is not valid')
        return False
