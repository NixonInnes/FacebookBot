from flask import Flask, request
import os
from .messenger import Messenger

VERIFY_TOKEN = os.getenv('MESSENGER_VERIFY_TOKEN', 'TEST_TOKEN_09345h349534985h3894h5398h')
FACEBOOK_TOKEN = os.getenv('FACEBOOK_TOKEN', 'EAAH9MS2hZCtYBAJKiWzoZBinOo6BtLqJ193KWw6zkQZAeH3dMhLGBB0PXVy7gMoZAbk8KZCowlBzEHnpZB4mhspx99NdR7Ts3QIDrpZCuE7rJhVZAaQzvWWlEu6JQ2ZBO9JSZAgtogGkCNo4px2eo1mAPP1Aoa1zjFOSmSm7s0ndkZBAly6dn7oob6o')

app = Flask(__name__)
messenger = Messenger(FACEBOOK_TOKEN)


@app.route("/messenger/webhook", methods=['GET', 'POST'])
def bot():
    if request == 'GET':
        token = request.args.get('hub.verify_token')
        if token == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        # log bad request

    if request == 'POST':
        post = request.json
        # log post
        events = post['entry'][0]['messaging']
        for event in events:
            if event.get('message', False):
                message = event['message'].get('text', None)
                sender_id = event['sender']
                messenger.send(sender_id, message)


if __name__ == '__main__':
    app.run(port=5000)
