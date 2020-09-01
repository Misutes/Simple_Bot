import random

import regex as re
import requests as rq

import Text as t


class Reply:

    def __init__(self, session, event):
        self.session = session
        self.event = event

    # Send message
    def sm(self, message, keyboard):
        self.session.method('messages.send', {
            'user_id': self.event.user_id,
            'message': message,
            "random_id": 0,
            "keyboard": keyboard
        })

    # Special send message
    def ssm(self, media_type, owner_id, media_id):
        owner_id = str(owner_id)
        media_id = str(media_id)
        media = f'{media_type}{owner_id}_{media_id}'
        self.session.method('messages.send', {
            'user_id': self.event.user_id,
            'attachment': media,
            'random_id': random.randint(0, 10 ** 10)
        })

    # Send free message
    def sfm(self, method, id, message):
        self.session.method(method, {
            "user_id": id,
            "message": message,
            "random_id": 0
        })

    # Massive send massage
    def msm(self, list_):
        for element in list_:
            self.sm(*element)

    # Delete message
    def dm(self):
        message_id = self.session.method('messages.getHistory', {
            'offset': 0,
            'count': 1,
            'user_id': t.administrator_id,
            'rev': 0})['items'][0]['id']

        self.session.method('messages.delete', {
            "message_ids": message_id,
            "group_id": '193464895',
            "delete_for_all": 1
        })

    # Edit message
    def em(self, message):
        self.session.method('messages.edit', {
            'peer_id': self.event.user_id,
            'message_id': self.event.message_id,
            'message': message
        })


class Request:

    def __init__(self, event):
        self.raw_message = event

    def clear(self):
        raw_list = (self.raw_message.lower()).split(' ')
        return [re.sub(r'[^\w\s]', '', word) for word in raw_list]


class Media:

    def __init__(self, session):
        self.session = session

    def upload(self, photo):
        upload_url = self.session.method('photos.getMessagesUploadServer')['upload_url']
        upload_photo = rq.post(upload_url, files={'photo': open(photo, 'rb')}).json()
        save_photo = self.session.method('photos.saveMessagesPhoto',
                                       {'server': upload_photo['server'], 'photo': upload_photo['photo'],
                                        'hash': upload_photo['hash']})[0]
        media_type = 'photo'
        owner_id = save_photo['owner_id']
        media_id = save_photo['id']
        media = (media_type, owner_id, media_id)
        return media
