from keyboard import new_keyboard
from challenge import start_challenge, book_challenge
from vk_api.longpoll import VkLongPoll, VkEventType

import json
import keyboard
import vk_api
import random
import Speech
import regex as re
import Text as t
import admin_command as ac
import litres as lr
import recommend as rc
import requests as rq
import dialogflow.google_ai as ai


token = '79eee7ae818b1db0d38b95f8911b1576e3d3a325c3622f6feaead4f3de1b09cdb0285cc9ac8308fb471f2'
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

user_list = []
user_check_dict = {}

empty = '&#4448;'

missunderstanding = {'меню литрес': [], 'что почитать': []}


def send_message(message, keyboard):
    vk_session.method('messages.send', {
        'user_id': event.user_id,
        'message': message,
        "random_id": 0,
        "keyboard": keyboard
    })


def stop_time_out():
    vk_session.method('messages.send', {
        'user_id': '122226430',
        'message': empty,
        "random_id": 0,
    })

# отправляет какое-либо вложение
def special_send_message(type, owner_id, media_id):
    owner_id = str(owner_id)
    media_id = str(media_id)
    media = f'{type}{owner_id}_{media_id}'
    vk_session.method('messages.send',
                      {'user_id': event.user_id, 'attachment': media, 'random_id': random.randint(0, 10 ** 10)})


# трансформирование входящего сообщения
def message_transform(element):
    return (element.lower()).split(' ')


# очистка слова от всех постаронних символов
def clear(word):
    return re.sub(r'[^\w\s]', '', word)

# загрузка изображений в скрытый альбом
def upload(photo):
    upload_url = vk_session.method('photos.getMessagesUploadServer')['upload_url']
    upload_photo = rq.post(upload_url, files={'photo': open(photo, 'rb')}).json()
    save_photo = vk_session.method('photos.saveMessagesPhoto',
                                   {'server': upload_photo['server'], 'photo': upload_photo['photo'],
                                    'hash': upload_photo['hash']})[0]
    type = 'photo'
    owner_id = save_photo['owner_id']
    media_id = save_photo['id']
    return type, owner_id, media_id


# загрузка необходимых изображений
hi_pic = [upload('pictures/hi_1.png'), upload('pictures/hi_2.png')]
dont_know = [upload('pictures/dont_know_1.png'), upload('pictures/dont_know_2.png')]
poster = upload('pictures/poster.png')
excursion = upload('pictures/excursion.png')
bye = upload('pictures/bye.png')


def main():
    global event
    while True:
        for event in longpoll.listen():
            greeting_pic = random.choice(hi_pic)
            if event.type == VkEventType.MESSAGE_NEW and event.from_me:
                # позволяет закончить общение, если написать "бот" или поставить на паузу
                if len([key for key in event.message_flags]) == 3:
                    ac.bot_return(vk_session, event, user_check_dict, special_send_message, greeting_pic)
            # создает переменную "непонятых слов", преобразует сообщение от пользователя и получает информацию о нем
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                miss = 0
                message = message_transform(event.text)
                user_message = [clear(word) for word in message]
                user_info = session_api.users.get(user_ids=event.user_id)
                user_info = user_info[0]
                # создает словарь с информацией о позиции пользоватедя: пауза, челендж, литрес
                user_check_dict.setdefault(user_info['id'],
                                           {'pause': 0, 'challenge': 0, 'litres': 0, 'recommendation': 0})
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
                # если человек внутри меню "литрес"
                elif user_check_dict[user_info['id']]['litres'] == 1:
                    lr.faq(event, user_message, user_info, send_message, special_send_message, user_check_dict, missunderstanding, bye)
                    # если внутри "литрес" захотел связаться с библиотекарем
                    if user_check_dict[user_info['id']]['pause'] == 1:
                        send_message(t.staff_answer, None)
                    break
                # если человек внутри меня "рекомендация"
                elif user_check_dict[user_info['id']]['recommendation'] == 1:
                    rc.recommend(event, user_message, user_info, send_message, special_send_message, user_check_dict, missunderstanding, bye)
                    break
                # если бот в "челлендже", отключает основные функции и работает по особому скрипту
                elif user_check_dict[user_info['id']]['challenge'] == 1:
                    book_challenge(user_message, send_message, empty, user_info, user_check_dict)
                    break
                # проверяет каждое слово в сообщении
                for word in user_message:
                    # если пользователь - администратор дает доступ к командам
                    if (user_info['id'] in ac.admin_id_list) and (word in ac.command_list):
                        ac.terminal(user_message, send_message)
                        break
                    # проверяет слова на наличие приветствия
                    if word in t.list_of_greeting:
                        greeting = random.choice(t.list_of_greeting_bot)
                        # если пользователь новый - бот представиться и добавит его в список пользователей
                        if user_info['id'] not in user_list:
                            user_list.append(user_info['id'])
                            special_send_message(*greeting_pic)
                            send_message(user_info['first_name'] + f', {greeting}' + t.first_greeting,
                                         new_keyboard(keyboard.function_keyboard))
                            send_message(t.speech, None)
                            send_message(t.connection, new_keyboard(keyboard.call_staff))
                        # иначе поприветствует его
                        else:
                            special_send_message(*greeting_pic)
                            send_message(user_info['first_name'] + f', {greeting}',
                                         new_keyboard(keyboard.function_keyboard))
                            send_message(t.connection, new_keyboard(keyboard.call_staff))
                    # если слово в списке команд "продления книги"
                    elif word in t.renewal_list:
                        send_message(user_info['first_name'] + t.renewal, new_keyboard(keyboard.link_keyboard))
                    # если слово в списке команд "узнать об адресе или времени работы "
                    elif word in t.time_list:
                        send_message(t.time, None)
                    # функция цитата дня
                    elif word in t.expression_call:
                        expression = random.choice(t.expression)
                        send_message(expression, None)
                    # экскурсии
                    elif word in t.excursion_call:
                        special_send_message(*excursion)
                        send_message(t.excursion, new_keyboard(keyboard.excursion_keyboard_one))
                        send_message(empty, new_keyboard(keyboard.excursion_keyboard_two))
                    # если слово в списке команд для работы с ЛитРес, выдает стартовое сообщение и отправляет пользователя в меню"Литрес"
                    elif word in t.litres_list:
                        user_check_dict[user_info['id']]['litres'] = 1
                        send_message(t.litres, new_keyboard(keyboard.litres_keyboard))
                        send_message(t.connection, new_keyboard(keyboard.call_staff))
                    # если слово в списке команд "О видио-лекция"
                    elif word in t.lectures:
                        send_message(user_info['first_name'] + t.lecture_message, None)
                        send_message(t.first_lecturer, new_keyboard(keyboard.first_lecture_keyboard))
                        send_message(t.second_lecturer, new_keyboard(keyboard.second_lecture_keyboard))
                        send_message(t.third_lecturer, new_keyboard(keyboard.third_lecture_keyboard))
                        send_message(t.fourth_lecturer, new_keyboard(keyboard.fourth_lecture_keyboard))
                    # Афиша
                    elif word in t.poster_call:
                        special_send_message(*poster)
                        send_message(t.poster, new_keyboard(keyboard.poster_keyboard))
                    # если слово в списке команд "Что почитать"
                    elif word in t.recommendation:
                        send_message(user_info['first_name'] + t.recomm_text,
                                     new_keyboard(keyboard.recommendation_keyboard))
                        user_check_dict[user_info['id']]['recommendation'] = 1
                    # если слово в списке команд "книжный челлендж", выдает сообщение и запускает скрипт челленджа
                    elif word in t.challenge_words:
                        user_check_dict[user_info['id']]['challenge'] = 1
                        start_challenge(vk_session, event, send_message, empty, user_info)
                    # Если интересно имя бота
                    elif word in t.name_call:
                        send_message(t.name, None)
                    # Если интересны создатели
                    elif word in t.creator_call:
                        send_message(t.creator, None)
                    # если пользователь хочет связаться с сотрудником
                    elif word in t.connection_list:
                        user_check_dict[user_info['id']]['pause'] = 1
                        send_message(t.staff_answer, None)
                    # если с ботоп прощаются или благодарят
                    elif word in t.parting:
                        special_send_message(*bye)
                    else:
                        miss += 1
                # если бот не понял все слова
                if miss == len(user_message):
                    respons = ai.response(event.text)
                    if respons == 'error':
                        dont = random.choice(dont_know)
                        special_send_message(*dont)
                        send_message(user_info['first_name'] + t.suggestion, new_keyboard(keyboard.function_keyboard))
                        send_message(t.connection, new_keyboard(keyboard.call_staff))
                    else:
                        send_message(respons, None)


print('Bot is ready!')


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print('Something going wrong.', e)
