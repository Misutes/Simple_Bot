import json
import random
import time
from datetime import datetime as dt

import vk_api
# from challenge import start_challenge, book_challenge
from vk_api.longpoll import VkLongPoll, VkEventType

import SQL
import Speech
import Text as t
import admin_command as ac
import dialogflow.google_ai as ai
import keyboard
import litres as lr
import mini_quiz as dq
import recommend as rc
from classes import Reply, Request, Media
from keyboard import new_keyboard

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
dovlatov_media = [(media.upload('pictures/dovlatov_secret_1.jpg'), media.upload('pictures/dovlatov_1.jpg')),
                  (media.upload('pictures/dovlatov_secret_2.jpg'), media.upload('pictures/dovlatov_2.jpg'))]


def main():
    database = SQL.Database()
    while True:
        for event in longpoll.listen():
            reply = Reply(session=vk_session, event=event)
            greeting_picture = random.choice(greeting_pictures)

            if event.type == VkEventType.MESSAGE_NEW and event.from_me:
                if len([key for key in event.message_flags]) == 3:
                    ac.terminal(vk_session, event, database, reply.ssm, greeting_picture)

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                database.insert_data('users', 'ID', event.user_id)
                database.update_name('users', 'NAME_', session_api.users.get(user_ids=event.user_id)[0]['first_name'], event.user_id)
                miss_word = 0
                user_message = Request(event.text).clear()
                user_name = str(database.find_data('users', 'NAME_', 'ID', event.user_id)[0])
                if event.attachments:
                    try:
                        reply.sm(message=t.recognition)
                        link = (json.loads(event.attachments['attachments']))[0]['audio_message']['link_mp3']
                        audio_message = Speech.audio_answer(link)
                        user_message = Request(audio_message).clear()
                    except KeyError:
                        reply.sm(message=t.non_recognition)

                if database.check_position('users', 'PAUSE', 1, event.user_id):
                    return

                elif database.check_position('users', 'LITRES', 1, event.user_id):
                    lr.litres(event, user_message, reply.sm, reply.ssm, database, bye)
                    if database.check_position('users', 'PAUSE', 1, event.user_id):
                        reply.sm(message=t.staff_answer)
                    return

                elif database.check_position('users', 'RECOMMENDATION', 1, event.user_id):
                    rc.recommend(event, user_message, reply.sm, reply.ssm, database, novelty, bye)
                    return

                elif database.check_position('users', 'QUIZ', 1, event.user_id):
                    dq.quiz(event, user_message, reply.sm, reply.ssm, database, dovlatov_media)
                    return

                # elif database.find_data('users', 'CHALLENGE', 1):
                # book_challenge(user_message, reply.sm, empty, user_info, database)
                # break

                for word in user_message:

                    if (event.user_id in ac.admin_ids) and (word in ac.command_list):
                        ac.terminal(vk_session, event, database, reply.ssm, greeting_picture)
                        return

                    if word in t.list_of_greeting:
                        greeting = random.choice(t.list_of_greeting_bot)
                        if database.check_position('users', 'NEW', 1, event.user_id):
                            database.update_data('users', 'NEW', 0, event.user_id)
                            reply.ssm(*greeting_picture)
                            new_user = [
                                (user_name + greeting + t.first_greeting, new_keyboard(keyboard.function_keyboard)),
                                (t.speech, None),
                                (t.connection, new_keyboard(keyboard.call_staff))
                            ]
                            reply.msm(new_user)
                        else:
                            reply.ssm(*greeting_picture)
                            greeting_list = [
                                (user_name + greeting, new_keyboard(keyboard.function_keyboard)),
                                (t.connection, new_keyboard(keyboard.call_staff))]
                            reply.msm(greeting_list)

                    elif word in t.renewal_list:
                        reply.sm(user_name + t.renewal, new_keyboard(keyboard.link_keyboard))

                    elif word in t.time_list:
                        reply.sm(t.time, new_keyboard(keyboard.sing_keyboard))

                    elif word in t.expression_call:
                        expression = random.choice(t.expression)
                        reply.sm(message=expression)

                    elif word in t.excursion_call:
                        reply.ssm(*excursion)
                        excursion_list = [
                            (t.excursion_one, new_keyboard(keyboard.excursion_keyboard_one)),
                            (t.empty, new_keyboard(keyboard.excursion_keyboard_two)),
                            (t.excursion_three, new_keyboard(keyboard.excursion_keyboard_three))
                        ]
                        reply.msm(excursion_list)

                    elif word in t.litres_list:
                        database.update_data('users', 'LITRES', 1, event.user_id)
                        litres_list = [
                            (t.litres, new_keyboard(keyboard.litres_keyboard)),
                            (t.connection, new_keyboard(keyboard.call_staff))]
                        reply.msm(litres_list)

                    elif word in t.lectures:
                        lecture = [
                            (user_name + t.lecture_message, None),
                            (t.first_lecturer, new_keyboard(keyboard.first_lecture_keyboard)),
                            (t.empty, new_keyboard(keyboard.first_lecture_two_keyboard)),
                            (t.second_lecturer, new_keyboard(keyboard.second_lecture_keyboard)),
                            (t.third_lecturer, new_keyboard(keyboard.third_lecture_keyboard)),
                            (t.fourth_lecturer, new_keyboard(keyboard.fourth_lecture_keyboard)),
                            (t.fifth_lecturer, new_keyboard(keyboard.fifth_lecture_keyboard))
                        ]
                        reply.msm(lecture)

                    elif word in t.poster_call:
                        reply.ssm(*poster)
                        reply.sm(t.poster, new_keyboard(keyboard.poster_keyboard))

                    elif word in t.recommendation:
                        reply.sm(user_name + t.recomm_text, new_keyboard(keyboard.recommendation_keyboard))
                        database.update_data('users', 'RECOMMENDATION', 1, event.user_id)

                    elif word in t.start_quiz:
                        if database.check_position('quiz', 'ID', event.user_id, event.user_id):
                            reply.sm(message=user_name + t.quiz_sorry)
                            break
                        database.update_data('quiz', 'QUESTION', 1, event.user_id)
                        database.update_data('users', 'QUIZ', 1, event.user_id)
                        database.insert_data('quiz', 'ID', event.user_id)
                        database.update_data('quiz', 'TIME_', int(time.time()), event.user_id)
                        reply.sm(message=user_name + t.quiz_start_text)
                        reply.sm(message=t.q_a[0][0])

                    # elif word in t.challenge_words:
                        # database.update_data('users', 'CHALLENGE', 1, event.user_id)
                        # start_challenge(vk_session, event, reply.sm, t.empty, user_info)

                    elif word in t.name_call:
                        reply.sm(message=t.name)

                    elif word in t.creator_call:
                        reply.sm(message=t.creator)

                    elif word in t.connection_list:
                        database.update_data('users', 'PAUSE', 1, event.user_id)
                        reply.sm(message=t.staff_answer)

                    elif word in t.parting:
                        reply.ssm(*bye)

                    else:
                        miss_word += 1

                if miss_word == len(user_message):
                    answer = ai.response(event.text)
                    if answer == 'error':
                        if not database.find_data('bag_words', 'MAIN_MENU', 'MAIN_MENU', event.text):
                            database.insert_data('bag_words', 'MAIN_MENU', event.text)
                        reply.ssm(*random.choice(confusion_pictures))
                        non_answer = [
                            (user_name + t.suggestion, new_keyboard(keyboard.function_keyboard)),
                            (t.connection, new_keyboard(keyboard.call_staff))
                        ]
                        reply.msm(non_answer)
                    else:
                        reply.sm(message=answer)


if __name__ == '__main__':
    restart = 'Restart at: '
    update = 'Я обновился! И работаю дальше, Создатель!'
    while True:
        try:
            print(restart + str(dt.now()))
            main()
        except Exception as e:
            print(str(dt.now()) + ': ' + str(e))
            vk_session.method('messages.send', {
                'user_id': t.administrator_id,
                'message': update,
                "random_id": 0,
                "keyboard": None
            })
            response = Reply(vk_session, next(longpoll.listen()))
            response.dm()
            print(str(dt.now()) + ': ' + update)


