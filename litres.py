import keyboard
from keyboard import new_keyboard
import Text as t


# меню ЛитРес
def faq(event, message, info, sm, ssm, database, media):
    miss = 0
    for word in message:
        # если пользователь хочет уйти, изменяет ему статус и отправляет сообщение
        if word == 'уйти':
            database.update_data('users', 'LITRES', 0, event.user_id)
            sm(info['first_name'] + t.quit, new_keyboard(keyboard.function_keyboard))
            sm(t.connection, new_keyboard(keyboard.call_staff))
        # пользователь хочет узнать "что такое ЛитРес"
        elif word == 'что':
            sm(t.litres_what, None)
        # пользователь хочет узнать "Как он работает"
        elif word == 'как':
            sm(t.litres_how, new_keyboard(keyboard.access_link))
        # если с ботоп прощаются или благодарят
        elif word in t.parting:
            ssm(*media)
        # пользователь хочет связаться с библиотекарем
        elif word in t.connection_list:
            database.update_data('users', 'LITRES', 0, event.user_id)
            database.update_data('users', 'PAUSE', 1, event.user_id)
        else:
            miss += 1
    if miss > len(message)-1:
        sm(t.help_litres, None)
        if not database.find_data('bag_words', 'LITRES', event.text):
            database.insert_data('bag_words', 'LITRES', event.text)

