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
user_check_dict = {}

empty = '&#4448;'


def send_message(message, keyboard):
    vk_session.method('messages.send', {
        'user_id': event.user_id,
        'message': message,
        "random_id": 0,
        "keyboard": keyboard
    })


# отправляет какое-либо вложение
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
                # позволяет закончить общение, если написать "бот"
                if len([key for key in event.message_flags]) == 3:
                    ac.bot_return(vk_session, event, user_check_dict)
            # создает переменную "непонятых слов", преобразует сообщение от пользователя и получает информацию о нем
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                miss = 0
                user_message = message_transform(event.text)
                user_info = session_api.users.get(user_ids=event.user_id)
                user_info = user_info[0]
                # создает словарь с информацией о позиции пользоватедя: пауза, челендж, литрес
                user_check_dict.setdefault(user_info['id'], {'pause': 0, 'challenge': 0, 'litres': 0})
                # пробует распознать голосовое сообщение и преобразовать его в текст
                if event.attachments:
                    try:
                        send_message(t.recognition, None)
                        link = (json.loads(event.attachments['attachments']))[0]['audio_message']['link_mp3']
                        audio_message = Speech.audio_answer(link)
                        user_message = message_transform(audio_message)
                    except KeyError:
                        pass
                # если человек выбрал "паузу", бот не будет отвечать
                if user_check_dict[user_info['id']]['pause'] == 1:
                    break
                # если бот в "челлендже", отключает основные функции и работает по особому скрипту
                if user_check_dict[user_info['id']]['challenge'] == 1:
                    book_challenge(user_message, send_message, empty, user_info, user_check_dict)
                    break
                # если человек внутри меню "литрес"
                if user_check_dict[user_info['id']]['litres'] == 1:
                    lr.faq(user_message, user_info, send_message, user_check_dict)
                    # если внутри "литрес" захотел связаться с библиотекарем
                    if user_check_dict[user_info['id']]['pause'] == 1:
                        send_message(t.staff_answer, None)
                    break
                # проверяет каждое слово в сообщении
                for word in user_message:
                    # если пользователь - администратор дает доступ к командам
                    if (user_info['id'] in ac.admin_id_list) and (word in ac.command_list):
                        ac.terminal(user_message, send_message)
                        break
                    # проверяет слова на наличие приветствия
                    if word in t.list_of_greeting:
                        # если пользователь новый - бот представиться и добавит его в список пользователей
                        if user_info['id'] not in user_list:
                            user_list.append(user_info['id'])
                            send_message(user_info['first_name'] + t.first_greeting, new_keyboard(keyboard.function_keyboard))
                            send_message(t.speech, None)
                            send_message(t.connection, new_keyboard(keyboard.call_staff))
                        # иначе поприветствует его
                        else:
                            send_message(
                                user_info['first_name'] + t.second_greeting,
                                new_keyboard(keyboard.function_keyboard))
                            send_message(t.connection, new_keyboard(keyboard.call_staff))
                    # если слово в списке команд "продления книги"
                    elif word in t.renewal_list:
                        send_message(user_info['first_name'] + t.renewal, new_keyboard(keyboard.link_keyboard))
                    # если слово в списке команд "узнать об адресе или времени работы "
                    elif word in t.time_list:
                        send_message(t.time, None)
                    # если слово в списке команд для работы с ЛитРес, выдает стартовое сообщение и отправляет пользователя в меню"Литрес"
                    elif word in t.litres_list:
                        user_check_dict[user_info['id']]['litres'] = 1
                        send_message(t.litres, new_keyboard(keyboard.litres_keyboard))
                        send_message(t.connection, new_keyboard(keyboard.call_staff))
                    # если слово в списке команд "О видио-лекция"
                    elif word in t.li:
                        send_message(user_info['first_name'] + t.lecture_message,
                                     None)
                        send_message(t.first_lecturer, new_keyboard(keyboard.olga_link_keyboard))
                        send_message(t.second_lecturer, new_keyboard(keyboard.unknown_link_keyboard))
                    # если слово в списке команд "Рекомендовации"
                    elif word in t.li2:
                        special_send_message('wall', -43349586, 7417)
                    # если слово в списке команд "книжный челлендж", выдает сообщение и запускает скрипт челленджа
                    elif word in t.challenge_words:
                        user_check_dict[user_info['id']]['challenge'] = 1
                        start_challenge(vk_session, event, send_message, empty, user_info)
                    # если пользователь хочет связаться с сотрудником
                    elif word in t.connection_list:
                        user_check_dict[user_info['id']]['pause'] = 1
                        send_message(t.staff_answer, None)
                    # если бот не понял слово в сообщении
                    else:
                        miss += 1
                # если бот не понял все слова
                if miss == len(user_message):
                    send_message(user_info['first_name'] + t.suggestion, new_keyboard(keyboard.function_keyboard))
                    send_message(t.connection, new_keyboard(keyboard.call_staff))


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print('Something going wrong.', e)