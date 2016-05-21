import requests
import json
from . import get_logger

logger = get_logger(__name__)

API_URL = "https://graph.facebook.com/v2.6/me"


class Button(object):
    def __init__(self, button_type, title, url_or_payload):
        self.type = button_type
        if self.type == 'web_url':
            self.url = url_or_payload
        elif self.type == 'postback':
            self.payload = url_or_payload
        else:
            raise Exception('Invalid button type defined. Specify "web_url", or "postback".')
        self.title = title

    def get_dict(self):
        elems = ['type', 'title', 'url', 'payload']
        return {elem: getattr(self, elem) for elem in elems if getattr(self, elem, None)}


class Image(object):
    def __init__(self, url):
        self.url = url

    def get_dict(self):
        return {'url': self.url}


class Element(object):
    def __init__(self, title, item_url=None, image_url=None, subtitle=None):
        self.title = title
        self.item_url = item_url
        self.image_url = image_url
        self.subtitle = subtitle
        self.buttons = []

    def add_button(self, button_type, title, url_or_payload):
        self.buttons.append(Button(button_type, title, url_or_payload))

    def get_dict(self):
        elems = ['title', 'item_url', 'image_url', 'subtitle']
        dict = {elem: getattr(self, elem) for elem in elems if getattr(self, elem, None)}
        dict['buttons'] = [button.get_dict() for button in self.buttons]
        return dict


class Template(object):
    def __init__(self, template_type, text=None):
        self.template_type = template_type
        if self.template_type == 'generic':
            self.elements = []
        elif self.template_type == 'button':
            self.text = text
            self.buttons = []
        else:
            raise Exception('Invalid Template type. Specify "generic", or "button".')

    def add_element(self, title, item_url=None, image_url=None, subtitle=None):
        self.elements.append(Element(title, item_url=item_url, image_url=image_url, subtitle=subtitle))

    def add_button(self, button_type, title, url_or_payload):
        self.buttons.append(Button(button_type, title, url_or_payload))

    def get_dict(self):
        elems = ['template_type', 'text']
        dict = {elem: getattr(self, elem) for elem in elems if getattr(self, elem, None)}
        if self.template_type == 'generic':
            dict['elements'] = [element.get_dict() for element in self.elements]
        if self.template_type == 'button':
            dict['buttons'] = [button.get_dict() for button in self.buttons]
        return dict


class Attachment(object):
    def __init__(self, attachment_type, url=None, template_type=None, text=None):
        self.type = attachment_type

        if self.type == 'image':
            self.payload = Image(url=url)
        elif self.type == 'template':
            self.payload = Template(template_type=template_type, text=text)
        else:
            raise Exception('Invalid Attachment type. Specify "image", or "template"')

    def get_dict(self):
        return {'type': self.type, 'payload': self.payload.get_dict()}


class Message(object):
    def __init__(self, text=None, attachment=None):
        self.text = text
        self.attachment = attachment

    def add_attachment(self, attachment_type, url=None, template_type=None, text=None):
        self.attachment = Attachment(attachment_type, url=url, template_type=template_type, text=text)

    def get_dict(self):
        dict = {}
        if self.text:
            dict['text'] = self.text
        if self.attachment:
            dict['attachment'] = self.attachment.get_dict()
        return dict


class Messenger(object):
    def __init__(self, token):
        self.access_token = token

    def subscribe(self):
        api_url = API_URL + '/subscribed_apps'
        params = {'access_token': self.access_token}
        return requests.post(api_url, params=params)

    def set_welcome(self, page_id, message):
        api_url = 'https://graph.facebook.com/v2.6/%s/thread_settings' % page_id
        headers = {'Content-Type': 'application/json'}
        params = {'access_token': self.access_token}
        data = {
            'setting_type': 'call_to_actions',
            'thread_state': 'new_thread',
            'call_to_actions': [
                {'message': json.dumps(message.get_dict())}
            ]
        }
        return requests.post(api_url, headers=headers, params=params, json=data)

    def send(self, recipient, message):
        api_url = API_URL + '/messages'
        headers = {'Content-Type': 'application/json'}
        params = {'access_token': self.access_token}
        data = {
            'recipient': {'id': recipient},
            'message': json.dumps(message.get_dict())
        }
        return requests.post(api_url, headers=headers, params=params, json=data)



