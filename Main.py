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


def send_message(message, keyboard):
    vk_session.method('messages.send', {
        'user_id': event.user_id,
        'message': message,
        "random_id": 0,
        "keyboard": keyboard
    })


def message_transform(element):
    return list((element.lower()).split(' '))


while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_message = message_transform(event.text)
            user_info = session_api.users.get(user_ids=event.user_id)
            user_info = user_info[0]
            if event.attachments:
                try:
                    send_message('Дайте-ка, подумать', None)
                    link = (json.loads(event.attachments['attachments']))[0]['audio_message']['link_mp3']
                    audio_message = Speech.audio_answer(link)
                    user_message = message_transform(audio_message)
                except KeyError:
                    pass
            if set(user_message) & set(Text.list_of_greeting):
                if user_info['id'] not in user_list:
                    user_list.append(user_info['id'])
                    send_message(user_info['first_name'] + Text.hello_message, new_keyboard(keyboard.function_keyboard))
                else:
                    send_message(user_info['first_name'] + str(', категорически приветствую! Напомниаю, что я могу: '),
                                 new_keyboard(keyboard.function_keyboard))
            elif 'продление' in user_message:
                send_message(user_info['first_name'] + str(', Вы можете сделать это здесь'),
                             new_keyboard(keyboard.link_keyboard))
            elif ('написать' and 'кое-что') in user_message:
                send_message(user_info['first_name'] + str(', я же умненький?'),
                             None)
            else:
                send_message(user_info['first_name'] + ', Климент Аркадьевич не умеет с этим работать.', None)