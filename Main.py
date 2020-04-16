import json
import keyboard
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import Speech
import Text
from keyboard import new_keyboard

token = '79eee7ae818b1db0d38b95f8911b1576e3d3a325c3622f6feaead4f3de1b09cdb0285cc9ac8308fb471f2'
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

user_list = []


def message(message, keyboard):
    vk_session.method('messages.send', {
        'user_id': event.user_id,
        'message': message,
        "random_id": 0,
        "keyboard": keyboard
    })


while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_message = list((event.text.lower()).split(' '))
            user_info = session_api.users.get(user_ids=event.user_id)
            user_info = user_info[0]
            if event.attachments:
                link = (json.loads(event.attachments['attachments']))[0]['audio_message']['link_mp3']
                message(Speech.audio_answer(link), None)
            if set(user_message) & set(Text.list_of_greeting):
                if user_info['id'] not in user_list:
                    user_list.append(user_info['id'])
                    message(user_info['first_name'] + Text.hello_message, new_keyboard(keyboard.function_keyboard))
                else:
                    message(user_info['first_name'] + str(', категорически приветствую! Напомниаю, что я могу: '),
                            new_keyboard(keyboard.function_keyboard))
            elif 'продление' in user_message:
                message(user_info['first_name'] + str(' , Вы можете сделать это здесь'),
                        new_keyboard(keyboard.link_keyboard))
            elif 'написать' and 'кое-что' in user_message:
                message(user_info['first_name'] + str(', я же умненький?'),
                        None)
