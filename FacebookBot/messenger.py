import requests

API_URL = "https://graph.facebook.com/v2.6/me/messages"


class Messenger(object):

    def __init__(self, token):
        self.access_token = token

    def send(self, recipient_id, message):
        headers = {'Content-Type': 'application/json'}
        params = {'access_token': self.access_token}
        json = {
            'recipient': {'id': recipient_id},
            'message': {'text': message}
        }

        response = requests.post(API_URL, headers=headers, params=params, json=json)

        #if not response.ok:
            # log error
            #pass

        return response.json()
