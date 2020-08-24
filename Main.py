from keyboard import new_keyboard
from challenge import start_challenge, book_challenge
from vk_api.longpoll import VkLongPoll, VkEventType
from classes import Reply, Request, Media
from datetime import datetime as dt

import threading
import time
import json
import keyboard
import vk_api
import random

import Speech
import Text as t
import admin_command as ac
import litres as lr
import recommend as rc
import dialogflow.google_ai as ai
import SQL

token = '79eee7ae818b1db0d38b95f8911b1576e3d3a325c3622f6feaead4f3de1b09cdb0285cc9ac8308fb471f2'
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# загрузка необходимых изображений
media = Media(vk_session)
greeting_pictures = [media.upload('pictures/hi_1.png'), media.upload('pictures/hi_2.png')]
confusion_pictures = [media.upload('pictures/dont_know_1.png'), media.upload('pictures/dont_know_2.png')]
poster = media.upload('pictures/poster.png')
excursion = media.upload('pictures/excursion.png')
bye = media.upload('pictures/bye.png')
novelty = media.upload('pictures/recommend.jpg')


def main():
    database = SQL.Database()
    while True:
        for event in longpoll.listen():
            reply = Reply(session=vk_session, event=event)
            greeting_picture = random.choice(greeting_pictures)
            if event.type == VkEventType.MESSAGE_NEW and event.from_me:
                # позволяет закончить общение, если написать "бот", или поставить на паузу
                if len([key for key in event.message_flags]) == 3:
                    ac.bot_return(vk_session, event, database, reply.ssm, greeting_picture)
            # создает переменную "непонятых слов", преобразует сообщение от пользователя и получает информацию о нем
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                miss = 0
                user_message = Request(event.text).clear()
                user_info = session_api.users.get(user_ids=event.user_id)[0]
                # пробует распознать голосовое сообщение и преобразовать его в текст
                if event.attachments:
                    try:
                        reply.sm(t.recognition, None)
                        link = (json.loads(event.attachments['attachments']))[0]['audio_message']['link_mp3']
                        audio_message = Speech.audio_answer(link)
                        user_message = Request(audio_message).clear()
                    except KeyError:
                        pass
                # если человек выбрал "паузу", бот не будет отвечать
                if database.check_position('users', 'PAUSE', 1, event.user_id):
                    break
                # если человек внутри меню "литрес"
                elif database.check_position('users', 'LITRES', 1, event.user_id):
                    lr.faq(event, user_message, user_info, reply.sm, reply.ssm, database, bye)
                    # если внутри "литрес" захотел связаться с библиотекарем
                    if database.check_position('users', 'PAUSE', 1, event.user_id):
                        reply.sm(t.staff_answer, None)
                    break
                # если человек внутри меня "рекомендация"

                elif database.check_position('users', 'RECOMMENDATION', 1, event.user_id):
                    rc.recommend(event, user_message, user_info, reply.sm, reply.ssm, database, novelty, bye)
                    break
                # если бот в "челлендже", отключает основные функции и работает по особому скрипту
                # elif database.find_data('users', 'CHALLENGE', 1):
                # book_challenge(user_message, reply.sm, empty, user_info, database)
                # break
                # проверяет каждое слово в сообщении
                for word in user_message:
                    # если пользователь - администратор дает доступ к командам
                    if (user_info['id'] in ac.admin_id_list) and (word in ac.command_list):
                        ac.terminal(user_message, reply.sm)
                        break
                    # проверяет слова на наличие приветствия
                    if word in t.list_of_greeting:
                        greeting = random.choice(t.list_of_greeting_bot)
                        # если пользователь новый - бот представиться и добавит его в список пользователей
                        if not database.find_data('users', 'ID', event.user_id):
                            database.insert_data('users', 'ID', event.user_id)
                            reply.ssm(*greeting_picture)
                            new_user = [
                                (user_info['first_name'] + f', {greeting}' + t.first_greeting,
                                 new_keyboard(keyboard.function_keyboard)),
                                (t.speech, None),
                                (t.connection, new_keyboard(keyboard.call_staff))
                            ]
                            reply.msm(new_user)
                        # иначе поприветствует его
                        else:
                            reply.ssm(*greeting_picture)
                            greeting_list = [
                                (user_info['first_name'] + f', {greeting}', new_keyboard(keyboard.function_keyboard)),
                                (t.connection, new_keyboard(keyboard.call_staff))]
                            reply.msm(greeting_list)

                    # если слово в списке команд "продления книги"
                    elif word in t.renewal_list:
                        reply.sm(user_info['first_name'] + t.renewal, new_keyboard(keyboard.link_keyboard))
                    # если слово в списке команд "узнать об адресе или времени работы "
                    elif word in t.time_list:
                        reply.sm(t.time, new_keyboard(keyboard.sing_keyboard))
                    # функция цитата дня
                    elif word in t.expression_call:
                        expression = random.choice(t.expression)
                        reply.sm(expression, None)
                    # экскурсии
                    elif word in t.excursion_call:
                        reply.ssm(*excursion)
                        excursion_list = [
                            (t.excursion_one, new_keyboard(keyboard.excursion_keyboard_one)),
                            (t.empty, new_keyboard(keyboard.excursion_keyboard_two)),
                            (t.excursion_three, new_keyboard(keyboard.excursion_keyboard_three))
                        ]
                        reply.msm(excursion_list)
                    # если слово в списке команд для работы с ЛитРес, выдает стартовое сообщение и отправляет пользователя в меню"Литрес"
                    elif word in t.litres_list:
                        database.update_data('users', 'LITRES', 1, event.user_id)
                        litres_list = [
                            (t.litres, new_keyboard(keyboard.litres_keyboard)),
                            (t.connection, new_keyboard(keyboard.call_staff))]
                        reply.msm(litres_list)
                    # если слово в списке команд "О видио-лекция"
                    elif word in t.lectures:

                        lecture = [
                            (user_info['first_name'] + t.lecture_message, None),
                            (t.first_lecturer, new_keyboard(keyboard.first_lecture_keyboard)),
                            (t.second_lecturer, new_keyboard(keyboard.second_lecture_keyboard)),
                            (t.third_lecturer, new_keyboard(keyboard.third_lecture_keyboard)),
                            (t.fourth_lecturer, new_keyboard(keyboard.fourth_lecture_keyboard)),
                            (t.fifth_lecturer, new_keyboard(keyboard.fifth_lecture_keyboard))
                        ]
                        reply.msm(lecture)
                    # Афиша
                    elif word in t.poster_call:
                        reply.ssm(*poster)
                        reply.sm(t.poster, new_keyboard(keyboard.poster_keyboard))
                    # если слово в списке команд "Что почитать"
                    elif word in t.recommendation:
                        reply.sm(user_info['first_name'] + t.recomm_text,
                                 new_keyboard(keyboard.recommendation_keyboard))
                        database.update_data('users', 'RECOMMENDATION', 1, event.user_id)
                    # если слово в списке команд "книжный челлендж", выдает сообщение и запускает скрипт челленджа
                    elif word in t.challenge_words:
                        database.update_data('users', 'CHALLENGE', 1, event.user_id)
                        start_challenge(vk_session, event, reply.sm, t.empty, user_info)
                    # Если интересно имя бота
                    elif word in t.name_call:
                        reply.sm(t.name, None)
                    # Если интересны создатели
                    elif word in t.creator_call:
                        reply.sm(t.creator, None)
                    # если пользователь хочет связаться с сотрудником
                    elif word in t.connection_list:
                        database.update_data('users', 'PAUSE', 1, event.user_id)
                        reply.sm(t.staff_answer, None)
                    # если с ботом прощаются или благодарят
                    elif word in t.parting:
                        reply.ssm(*bye)
                    else:
                        miss += 1
                # если бот не понял все слова
                if miss == len(user_message):
                    answer = ai.response(event.text)
                    if answer == 'error':
                        if not database.find_data('bag_words', 'MAIN_MENU', event.text):
                            database.insert_data('bag_words', 'MAIN_MENU', event.text)
                        reply.ssm(*random.choice(confusion_pictures))
                        non_answer = [
                            (user_info['first_name'] + t.suggestion, new_keyboard(keyboard.function_keyboard)),
                            (t.connection, new_keyboard(keyboard.call_staff))
                        ]
                        reply.msm(non_answer)
                    else:
                        reply.sm(answer, None)


ready = 'Bot is ready!'
print(ready)


def sleep_breaker():
    response = Reply(vk_session, next(longpoll.listen()))
    message = 'Я обновился! И работаю дальше, Создатель!'
    while True:
        response.sfm('messages.send', t.administrator_id, message)
        response.dm()
        time.sleep(10800)


if __name__ == '__main__':
    try:
        main_thread = threading.Thread(target=main)
        timer_thread = threading.Thread(target=sleep_breaker)
        main_thread.start()
        timer_thread.start()
    except Exception as e:
        print(str(dt.now()) + ':\n' + str(e))
