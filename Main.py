import json
import keyboard
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import random
import Speech
import Text as t
import admin_command as ac
import litres as lr
from keyboard import new_keyboard
from challenge import start_challenge, book_challenge

token = '79eee7ae818b1db0d38b95f8911b1576e3d3a325c3622f6feaead4f3de1b09cdb0285cc9ac8308fb471f2'
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

user_list = []
bot_pause_dict = {}
challenge_dict = {}
litres_dict = {}

empty = '&#4448;'


def send_message(message, keyboard):
    vk_session.method('messages.send', {
        'user_id': event.user_id,
        'message': message,
        "random_id": 0,
        "keyboard": keyboard
    })


def special_send_message(type, owner_id, media_id):
    owner_id = str(owner_id)
    media_id = str(media_id)
    media = f'{type}{owner_id}_{media_id}'
    vk_session.method('messages.send',
                      {'user_id': event.user_id, 'attachment': media, 'random_id': random.randint(0, 10 ** 10)})


def message_transform(element):
    return (element.lower()).split(' ')


def main():
    global event
    while True:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.from_me:
                if len([key for key in event.message_flags]) == 3:
                    ac.bot_return(vk_session, event, bot_pause_dict)
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                miss = 0
                user_message = message_transform(event.text)
                user_info = session_api.users.get(user_ids=event.user_id)
                user_info = user_info[0]
                bot_pause_dict.setdefault(user_info['id'], 0)
                challenge_dict.setdefault(user_info['id'], 0)
                litres_dict.setdefault(user_info['id'], 0)
                if event.attachments:
                    try:
                        send_message('Дайте-ка, подумать', None)
                        link = (json.loads(event.attachments['attachments']))[0]['audio_message']['link_mp3']
                        audio_message = Speech.audio_answer(link)
                        user_message = message_transform(audio_message)
                    except KeyError:
                        pass
                if bot_pause_dict[user_info['id']] == 1:
                    break
                if challenge_dict[user_info['id']] == 1:
                    book_challenge(user_message, send_message, empty, user_info, challenge_dict)
                    break
                if litres_dict[user_info['id']] == 1:
                    lr.faq(user_message, user_info, send_message, empty, bot_pause_dict, litres_dict)
                    if bot_pause_dict[user_info['id']] == 1:
                        send_message(t.staff_answer, None)
                    break
                for word in user_message:
                    if (user_info['id'] in ac.admin_id_list) and (word in ac.command_list):
                        ac.terminal(user_message, send_message)
                        break
                    if word in t.list_of_greeting:
                        if user_info['id'] not in user_list:
                            user_list.append(user_info['id'])
                            send_message(user_info['first_name'] + t.first_greeting, new_keyboard(keyboard.function_keyboard))
                            send_message(t.speech, None)
                            send_message(t.connection, new_keyboard(keyboard.call_staff))
                        else:
                            send_message(
                                user_info['first_name'] + t.second_greeting,
                                new_keyboard(keyboard.function_keyboard))
                            send_message(t.connection, new_keyboard(keyboard.call_staff))
                    elif word in t.renewal_list:
                        send_message(user_info['first_name'] + t.renewal, new_keyboard(keyboard.link_keyboard))
                    elif word in t.time_list:
                        send_message(t.time, None)
                    elif word in t.litres_list:
                        litres_dict[user_info['id']] = 1
                        send_message(t.litres, new_keyboard(keyboard.litres_keyboard))
                        send_message(t.connection, new_keyboard(keyboard.call_staff))
                    elif word == 'видео-лекции':
                        send_message(user_info['first_name'] + str(', вот что у нас есть.'),
                                     None)
                        send_message('Лектор: Ольга Сергеевна Сапанжа', new_keyboard(keyboard.olga_link_keyboard))
                        send_message('Лектор: ???', new_keyboard(keyboard.unknown_link_keyboard))
                    elif word == 'рекомендация':
                        special_send_message('wall', -43349586, 7417)
                    elif word == ('книжный' or 'вызов'):
                        challenge_dict[user_info['id']] = 1
                        start_challenge(vk_session, event, send_message, empty, user_info)
                    elif word in t.connection_list:
                        bot_pause_dict[user_info['id']] = 1
                        send_message(t.staff_answer, None)
                    else:
                        miss += 1
                if miss == len(user_message):
                    send_message(
                        user_info['first_name'] + t.suggestion,
                        new_keyboard(keyboard.function_keyboard))
                    send_message(t.connection, new_keyboard(keyboard.call_staff))


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print('Something going wrong.', e)