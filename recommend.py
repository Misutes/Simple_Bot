import keyboard
from keyboard import new_keyboard
import Text as t
import random


# меню Что почитать?
def recommend(event, message, info, send_func, special, user_check_dict, bag_dict, media):
    miss = 0
    for word in message:
        # если пользователь хочет уйти, изменяет ему статус и отправляет сообщение
        if word == 'уйти':
            user_check_dict[info['id']]['recommendation'] = 0
            send_func(info['first_name'] + t.quit, new_keyboard(keyboard.function_keyboard))
            send_func(t.connection, new_keyboard(keyboard.call_staff))
        # пользователь хочет узнать о "Новинках"
        elif word == 'новинки':
            special('wall', t.group_id, '7712')
        # пользователь хочет узнать книги из категории "Фантастика"
        elif word == 'фантастика':
            send_func(t.fantastic_literature, None)
            special('wall', t.group_id, random.choice(t.fantastic))
        # пользователь хочет узнать книги из категории "Япония"
        elif word == 'япония':
            send_func(t.japan_literature, None)
            special('wall', t.group_id, random.choice(t.japan))
        # пользователь хочет узнать книги из категории "Детективы"
        elif word == 'детективы':
            send_func(t.detective_literature, None)
            special('wall', t.group_id, random.choice(t.detective))
        # пользователь хочет узнать что ему рекомендуют
        elif word == 'климент':
            special('photo', t.group_id, '457249686')
            send_func(t.recommendation_description, new_keyboard(keyboard.recommendation_link))
        # если с ботоп прощаются или благодарят
        elif word in t.parting:
            special(*media)
        else:
            miss += 1
    # ответ на неизвестную команду
    if miss > len(message)-1:
        send_func(t.help, None)
        if event.text not in bag_dict['что почитать']:
            bag_dict['что почитать'].append(event.text)
        print(bag_dict)
