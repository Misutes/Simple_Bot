import keyboard
from keyboard import new_keyboard
import Text as t
import random


# меню Что почитать?
def recommend(event, message, info, sm, ssm, database, media_1, media_2):
    miss = 0
    for word in message:
        # если пользователь хочет уйти, изменяет ему статус и отправляет сообщение
        if word == 'уйти':
            database.update_data('users', 'RECOMMENDATION', 0, event.user_id)
            sm(info['first_name'] + t.quit, new_keyboard(keyboard.function_keyboard))
            sm(t.connection, new_keyboard(keyboard.call_staff))
        # пользователь хочет узнать о "Новинках"
        elif word == 'новинки':
            sm(t.novelty, new_keyboard(keyboard.novelty_bookshelf_link))
        # пользователь хочет узнать книги из категории "Фантастика"
        elif word == 'фантастика':
            sm(t.fantastic_literature, None)
            ssm('wall', t.group_id, random.choice(t.fantastic))
        # пользователь хочет узнать книги из категории "Япония"
        elif word == 'япония':
            sm(t.japan_literature, None)
            ssm('wall', t.group_id, random.choice(t.japan))
        # пользователь хочет узнать книги из категории "Детективы"
        elif word == 'детективы':
            sm(t.detective_literature, None)
            ssm('wall', t.group_id, random.choice(t.detective))
        # пользователь хочет узнать книги из категории "Подростковая"
        elif word == 'подростковая':
            sm(t.teen, new_keyboard(keyboard.teen_bookshelf_link))
        # пользователь хочет узнать что ему рекомендуют
        elif word == 'климент':
            ssm(*media_1)
            sm(t.recommendation_description, new_keyboard(keyboard.recommendation_link))
        # если с ботоп прощаются или благодарят
        elif word in t.parting:
            ssm(*media_2)
        else:
            miss += 1
    # ответ на неизвестную команду
    if miss > len(message)-1:
        sm(t.help_recommendation, None)
        if not database.find_data('bag_words', 'RECOMMENDATION', event.text):
            database.insert_data('bag_words', 'RECOMMENDATION', event.text)