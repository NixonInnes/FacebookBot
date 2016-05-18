from flask import Flask, request
import os
from .messenger import Messenger

VERIFY_TOKEN = os.getenv('MESSENGER_VERIFY_TOKEN', 'TEST_TOKEN_09345h349534985h3894h5398h')
FACEBOOK_TOKEN = os.getenv('FACEBOOK_TOKEN', 'EAAH9MS2hZCtYBAJKiWzoZBinOo6BtLqJ193KWw6zkQZAeH3dMhLGBB0PXVy7gMoZAbk8KZCowlBzEHnpZB4mhspx99NdR7Ts3QIDrpZCuE7rJhVZAaQzvWWlEu6JQ2ZBO9JSZAgtogGkCNo4px2eo1mAPP1Aoa1zjFOSmSm7s0ndkZBAly6dn7oob6o')

app = Flask(__name__)
messenger = Messenger(FACEBOOK_TOKEN)


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
            if event.get('message', False) and event.get('sender', False):
                message = event['message'].get('text')
                sender_id = event['sender'].get('id')
                messenger.send(sender_id, message)
        return '', 200


if __name__ == '__main__':
    ssl_context = ('certs/fullchain.pem', 'certs/privkey.pem')
    app.run(host='0.0.0.0', port=5000, ssl_context=ssl_context)
