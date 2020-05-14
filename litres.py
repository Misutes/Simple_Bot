import keyboard
from keyboard import new_keyboard
import Text as t


def faq(message, info, send_func, empty, pause_list, quit_list):
    faq_var = True
    for word in message:
        if word == 'уйти':
            faq_var = False
            quit_list[info['id']] = 0
            send_func(info['first_name'] + t.suggestion,
                      new_keyboard(keyboard.function_keyboard))
        elif word == 'что':
            send_func(t.litres_what, None)
        elif word == 'как':
            send_func(t.litres_how, new_keyboard(keyboard.access_link))
        elif word in t.connection_list:
            quit_list[info['id']] = 0
            pause_list[info['id']] = 1

    if faq_var and pause_list[info['id']] == 0:
        send_func(t.litres_sub, new_keyboard(keyboard.litres_keyboard))
        send_func(t.connection, new_keyboard(keyboard.call_staff))