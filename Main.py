# -*- coding: utf-8 -*-

import json
import random
import time
import requests
from datetime import datetime as dt

import vk_api
# from challenge import start_challenge, book_challenge
from vk_api.longpoll import VkLongPoll, VkEventType

import SQL
import Speech
import admin_command as ac
import dialogflow.google_ai as ai
import litres as lr
import mini_quiz as dq
import recommend as rc
from classes import Reply, Request, Media, JsonTable
import keyboard as kb

token = '79eee7ae818b1db0d38b95f8911b1576e3d3a325c3622f6feaead4f3de1b09cdb0285cc9ac8308fb471f2'
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

media = Media(vk_session)
greeting_pictures = [media.upload('pictures/hi_1.png'), media.upload('pictures/hi_2.png')]
confusion_pictures = [media.upload('pictures/dont_know_1.png'), media.upload('pictures/dont_know_2.png')]
poster = media.upload('pictures/poster.png')
excursion = media.upload('pictures/excursion.png')
bye = media.upload('pictures/bye.png')
novelty = media.upload('pictures/recommend.jpg')
ya_picture = media.upload('pictures/ya_bookshelf.png')
dovlatov_media = [(media.upload('pictures/dovlatov_secret_1.jpg'), media.upload('pictures/dovlatov_1.jpg')),
                  (media.upload('pictures/dovlatov_secret_2.jpg'), media.upload('pictures/dovlatov_2.jpg'))]


def main():
    database = SQL.Database()

    def greet():
        greeting = random.choice(jsonTable.get_text('greeting_list'))
        if database.check_position('users', 'NEW', 1, reply.event.user_id):
            database.update_data('users', 'NEW', 0, reply.event.user_id)
            reply.ssm(*greeting_picture)
            new_user = [
                (user_name + greeting + jsonTable.get_text('first_meeting'), kb.main_menu),
                (jsonTable.get_text('speech'), None),
                (jsonTable.get_text('staff_connect'), kb.staff_call)
            ]
            reply.msm(new_user)
        else:
            reply.ssm(*greeting_picture)
            greeting_list = [
                (user_name + greeting, kb.main_menu),
                (jsonTable.get_text('staff_connect'), kb.staff_call)]
            reply.msm(greeting_list)

    def gratitude():
        reply.ssm(*bye)

    def name_introduce():
        reply.sm(message=jsonTable.get_text('name'))

    def creator_introduce():
        reply.sm(message=jsonTable.get_text('creator'))

    def staff_call():
        database.update_data('users', 'PAUSE', 1, event.user_id)
        reply.sm(message=jsonTable.get_text('await_staff'))

    def book_renewal():
        reply.sm(user_name + jsonTable.get_text('renewal_book'), kb.renewal_book)

    def schedule_introduce():
        reply.sm(jsonTable.get_text('time_address'), kb.geo_position)

    def get_quote():
        expression = random.choice(jsonTable.get_text('quotes_list'))
        reply.sm(message=expression)

    def get_excursion():
        reply.ssm(*excursion)
        excursion_list = [
            (jsonTable.get_text('excursion_one'), kb.excursion),
            (jsonTable.get_text('empty'), kb.excursion_two),
            (jsonTable.get_text('excursion_two'), kb.excursion_three)
        ]
        reply.msm(excursion_list)

    def get_litres():
        database.update_data('users', 'LITRES', 1, event.user_id)
        litres_list = [
            (jsonTable.get_text('litres'), kb.litres_menu),
            (jsonTable.get_text('staff_connect'), kb.staff_call)]
        reply.msm(litres_list)

    def get_lecture():
        lecture = [
            (user_name + jsonTable.get_text('announce_lecturer'), None),
            (jsonTable.get_text('first_lecturer'), kb.first_lecturer),
            (jsonTable.get_text('empty'), kb.first_lecturer_two),
            (jsonTable.get_text('second_lecturer'), kb.second_lecturer),
            (jsonTable.get_text('third_lecturer'), kb.third_lecturer),
            (jsonTable.get_text('fourth_lecturer'), kb.fourth_lecturer),
            (jsonTable.get_text('fifth_lecturer'), kb.fifth_lecturer)
        ]
        reply.msm(lecture)

    def get_poster():
        reply.ssm(*poster)
        reply.sm(jsonTable.get_text('events'), kb.poster)

    def get_book():
        reply.sm(user_name + jsonTable.get_text('bookshelf'), kb.bookshelf_menu)
        database.update_data('users', 'RECOMMENDATION', 1, event.user_id)

    def start_mini_quiz():
        if database.check_position('quiz', 'ID', event.user_id, event.user_id):
            reply.sm(message=user_name + jsonTable.get_text('quiz_sorry'))
            return
        database.update_data('quiz', 'QUESTION', 1, event.user_id)
        database.update_data('users', 'QUIZ', 1, event.user_id)
        database.insert_data('quiz', 'ID', event.user_id)
        database.update_data('quiz', 'TIME_', int(time.time()), event.user_id)
        reply.sm(message=user_name + jsonTable.get_text('quiz_start_text'))
        reply.sm(message=jsonTable.get_text('q_a')[0][0])

    def none_answer():
        answer = ai.response(event.text)
        if answer == 'error':
            if not database.find_data('bag_words', 'MAIN_MENU', 'MAIN_MENU', event.text):
                database.insert_data('bag_words', 'MAIN_MENU', event.text)
            reply.ssm(*random.choice(confusion_pictures))
            non_answer = [
                (user_name + jsonTable.get_text('suggestion'), kb.main_menu),
                (jsonTable.get_text('staff_connect'), kb.staff_call)
            ]
            reply.msm(non_answer)
        else:
            reply.sm(message=answer)

    def _pass_():
        pass

    key_function = {
        "greet": greet,
        "gratitude": gratitude,
        "name_introduce": name_introduce,
        "creator_introduce": creator_introduce,
        "staff_call": staff_call,
        "book_renewal": book_renewal,
        "schedule_introduce": schedule_introduce,
        "get_litres": get_litres,
        "get_lecture": get_lecture,
        "get_book": get_book,
        "get_poster": get_poster,
        "get_quote": get_quote,
        "get_excursion": get_excursion,
        "none": none_answer,
        "pass": _pass_
    }

    jsonTable = JsonTable(key_function)

    while True:
        for event in longpoll.listen():
            reply = Reply(session=vk_session, event=event)
            greeting_picture = random.choice(greeting_pictures)

            if event.type == VkEventType.MESSAGE_NEW and event.from_me:
                if len([key for key in event.message_flags]) == 3:
                    ac.terminal(vk_session, event, jsonTable, database, reply.ssm, greeting_picture)

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                database.insert_data('users', 'ID', event.user_id)
                database.update_name('users', 'NAME_', session_api.users.get(user_ids=event.user_id)[0]['first_name'], event.user_id)
                user_message = Request(event.text).clear()
                user_name = str(database.find_data('users', 'NAME_', 'ID', event.user_id)[0])
                if event.attachments:
                    try:
                        reply.sm(message=jsonTable.get_text('recognition'))
                        link = (json.loads(event.attachments['attachments']))[0]['audio_message']['link_mp3']
                        audio_message = Speech.audio_answer(link)
                        user_message = Request(audio_message).clear()
                    except KeyError:
                        reply.sm(message=jsonTable.get_text('non_recognition'))
                global_variables = (event, jsonTable, user_message, reply.sm, reply.ssm, database)
                if database.check_position('users', 'PAUSE', 1, event.user_id):
                    return

                elif database.check_position('users', 'LITRES', 1, event.user_id):
                    lr.litres(*global_variables, bye)
                    if database.check_position('users', 'PAUSE', 1, event.user_id):
                        reply.sm(message=jsonTable.get_text('await_staff'))
                    return

                elif database.check_position('users', 'RECOMMENDATION', 1, event.user_id):
                    rc.recommend(*global_variables, novelty, bye, ya_picture)
                    return

                elif database.check_position('users', 'QUIZ', 1, event.user_id):
                    dq.quiz(*global_variables, dovlatov_media)
                    return

                if (event.user_id in ac.admin_ids) and (user_message in ac.command_list):
                    ac.terminal(vk_session, event, database, reply.ssm, greeting_picture)
                    return
                jsonTable.search_answer(user_message)


if __name__ == '__main__':
    restart = 'Restart at: '
    update = 'Я обновился! И работаю дальше, Создатель!'
    reconnect = 'Переподключение к серверам ВК'

    def update_(sleep_time,  exception):
        print(date_time + ': ' + exception)
        time.sleep(sleep_time)
        vk_session.method('messages.send', {
            'user_id': "122226430",
            'message': update,
            "random_id": 0,
            "keyboard": None
        })
        response = Reply(vk_session, next(longpoll.listen()))
        response.dm()
        print(date_time + ': ' + update)
    while True:
        H = int(dt.now().strftime("%H")) + 3
        date_time = dt.now().strftime(f"%d/%m/%Y, {H}:%M:%S")
        try:
            main()
        except requests.exceptions.ReadTimeout:
            update_(70, reconnect)
        except Exception as e:
            update_(5, e)
        else:
            print(restart + date_time)

