import keyboard
from keyboard import new_keyboard
import Text as t


# меню ЛитРес
def faq(message, info, send_func, user_check_dict):
    miss = 0
    for word in message:
        # если пользователь хочет уйти, изменяет ему статус и отправляет сообщение
        if word == 'уйти':
            user_check_dict[info['id']]['litres'] = 0
            send_func(info['first_name'] + t.quit, new_keyboard(keyboard.function_keyboard))
            send_func(t.connection, new_keyboard(keyboard.call_staff))
        # пользователь хочет узнать "что такое ЛитРес"
        elif word == 'что':
            send_func(t.litres_what, None)
        # пользователь хочет узнать "Как он работает"
        elif word == 'как':
            send_func(t.litres_how, new_keyboard(keyboard.access_link))
        # пользователь хочет связаться с библиотекарем
        elif word in t.connection_list:
            user_check_dict[info['id']]['litres'] = 0
            user_check_dict[info['id']]['pause'] = 1
        else:
            miss += 1
    if miss > len(message)-1:
        send_func(t.help, None)

