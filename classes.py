import random
import json

import regex as re
import requests as rq


class Reply:

    def __init__(self, session, event):
        self.session = session
        self.event = event

    # Send message
    def sm(self, message="&#4448;", keyboard=None):
        self.session.method('messages.send', {
            'user_id': self.event.user_id,
            'message': message,
            "random_id": 0,
            "keyboard": keyboard
        })

    # Special send message
    def ssm(self, media):
        self.session.method('messages.send', {
            'user_id': self.event.user_id,
            'attachment': media,
            'random_id': random.randint(0, 10 ** 10)
        })

    # Send free message
    def sfm(self, method, user_id, message):
        self.session.method(method, {
            "user_id": user_id,
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
            'user_id': "122226430",
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
        raw_list = [re.sub(r'[^\w\s]', '', word) for word in raw_list]
        return [re.sub(r'[quot]', '', word) for word in raw_list]


class Media:

    def __init__(self, session):
        self.session = session

    def upload(self, media, type_='photo'):
        if type_ == 'photo':
            upload_url = self.session.method('photos.getMessagesUploadServer')['upload_url']
            upload_photo = rq.post(upload_url, files={'photo': open(media, 'rb')}).json()
            save_photo = self.session.method('photos.saveMessagesPhoto',
                                             {'server': upload_photo['server'], 'photo': upload_photo['photo'],
                                              'hash': upload_photo['hash']})[0]
            media_address = '{}{}_{}'.format(type_, save_photo['owner_id'], save_photo['id'])
            return media_address

        upload_url = self.session.method("docs.getMessagesUploadServer",
                                         {"type": "audio_message", 'peer_id': '89546661'})
        upload_audio = rq.post(upload_url['upload_url'], files={'file': open(media, 'rb')}).json()
        save_audio = self.session.method("docs.save", {"file": upload_audio['file']})['audio_message']
        media_address = '{}{}_{}'.format(type_, save_audio['owner_id'], save_audio['id'])
        return media_address


class JsonTable:

    def __init__(self, key_function):
        with open('key_words.json', 'r', encoding="cp1251") as keys_file:
            self.key_words = json.load(keys_file)

        with open('text.json', 'r', encoding="cp1251") as text_file:
            self.text = json.load(text_file)

        with open('media_address.json', 'r', encoding="cp1251") as audio_file:
            self.medias = json.load(audio_file)

        self.key_function = key_function

    def search_answer(self, user_message):
        miss_word = True
        for word in user_message:
            try:
                self.key_function[self.key_words[word]]()
                miss_word = False
            except:
                pass
        if miss_word:
            self.key_function["none"]()

    def get_data(self, key, data='text'):
        return self.text[key] if data == 'text' else self.medias[key]


def create_table(name, dict_):
    with open(name, 'w', encoding="cp1251") as file:
        json.dump(dict_, file, ensure_ascii=False)
