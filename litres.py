import keyboard
from keyboard import new_keyboard
import Text as t

# меню ЛитРес
def faq(message, info, send_func, user_check_dict):
    faq_var = True
    for word in message:
        # если пользователь хочет уйти, изменяет ему статус и отправляет сообщение
        if word == 'уйти':
            faq_var = False
            user_check_dict[info['id']]['litres'] = 0
            send_func(info['first_name'] + t.suggestion, new_keyboard(keyboard.function_keyboard))
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
    # отправляет после кажого выбора из меню выше, пока не нажата кнопка "уйти"
    if faq_var and user_check_dict[info['id']]['pause'] == 0:
        send_func(t.litres_sub, new_keyboard(keyboard.litres_keyboard))
        send_func(t.connection, new_keyboard(keyboard.call_staff))