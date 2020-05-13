import json
import keyboard
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import Speech
import Text
from keyboard import new_keyboard
from challenge import start_challenge, book_challenge

token = '79eee7ae818b1db0d38b95f8911b1576e3d3a325c3622f6feaead4f3de1b09cdb0285cc9ac8308fb471f2'
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

user_list = []
bot_pause_dict = {}
challenge_dict = {}

empty = '&#4448;'


def send_message(message, keyboard):
    vk_session.method('messages.send', {
        'user_id': event.user_id,
        'message': message,
        "random_id": 0,
        "keyboard": keyboard
    })


def message_transform(element):
    return (element.lower()).split(' ')


def bot_return():
    global event
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.from_me:
            if 'бот' == event.text.lower():
                vk_session.method('messages.edit', {'peer_id': event.user_id, 'message_id': event.message_id,
                                                    'message': 'Спасибо за обращение!'})

                break


def main():
    global event
    while True:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.from_me:
                if len([key for key in event.message_flags]) == 3:
                    bot_return()
                    bot_pause_dict[event.user_id] = 0
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                miss = 0
                user_message = message_transform(event.text)
                user_info = session_api.users.get(user_ids=event.user_id)
                user_info = user_info[0]
                bot_pause_dict.setdefault(user_info['id'], 0)
                challenge_dict.setdefault(user_info['id'], 0)
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
                    book_challenge(user_message, send_message, empty, message_transform, user_info, challenge_dict)
                    break
                for word in user_message:
                    if word in Text.list_of_greeting:
                        if user_info['id'] not in user_list:
                            user_list.append(user_info['id'])
                            send_message(user_info['first_name'] + Text.hello_message,
                                         new_keyboard(keyboard.function_keyboard))
                            send_message('А еще я умею понимать голосовые сообщения!\n'
                                         'Попробуйте!', None)
                        else:
                            send_message(
                                user_info['first_name'] + str(', категорически приветствую! Напомниаю, что я могу: '),
                                new_keyboard(keyboard.function_keyboard))
                    elif word in Text.renewal_list:
                        send_message(user_info['first_name'] + str(', Вы можете продлить книги здесь'),
                                     new_keyboard(keyboard.link_keyboard))
                    elif word == 'видео-лекции':
                        send_message(user_info['first_name'] + str(', вот что у нас есть.'),
                                     None)
                        send_message('Лектор: Ольга Сергеевна Сапанжа', new_keyboard(keyboard.olga_link_keyboard))
                        send_message('Лектор: ???', new_keyboard(keyboard.unknown_link_keyboard))
                    elif word == 'рекомендация':
                        send_message(empty, new_keyboard(keyboard.recommend_link_keyboard))
                    elif word == ('книжный' or 'вызов'):
                        challenge_dict[user_info['id']] = 1
                        start_challenge(vk_session, event, send_message, empty, user_info)
                    else:
                        miss += 1
                if ('сотрудником' in user_message) or ('связаться' in user_message):
                    bot_pause_dict[user_info['id']] = 1
                elif miss == len(user_message):
                    send_message(
                        user_info['first_name'] + ', Климент Аркадьевич может предложить',
                        new_keyboard(keyboard.function_keyboard))
                    send_message('Или Вы можете связаться с сотрудником билиотеки', new_keyboard(keyboard.call_staff))


if __name__ == '__main__':
    main()
