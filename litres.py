import Text as t
import keyboard
from keyboard import new_keyboard

quit_ = ['уйти']
what_read = ['что']
access = ['как']


def litres(event, message, sm, ssm, database, media):
    miss_word = 0
    user_name = str(database.find_data('users', 'NAME_', 'ID', event.user_id)[0])
    for word in message:

        if word in quit_:
            database.update_data('users', 'LITRES', 0, event.user_id)
            sm(user_name + t.quit, new_keyboard(keyboard.function_keyboard))
            sm(t.connection, new_keyboard(keyboard.call_staff))

        elif word in what_read:
            sm(t.litres_what, None)

        elif word in access:
            sm(t.litres_how, new_keyboard(keyboard.access_link))

        elif word in t.parting:
            ssm(*media)

        elif word in t.connection_list:
            database.update_data('users', 'LITRES', 0, event.user_id)
            database.update_data('users', 'PAUSE', 1, event.user_id)

        else:
            miss_word += 1

    if miss_word > len(message)-1:
        sm(t.help_litres, None)
        if not database.find_data('bag_words', 'LITRES', 'LITRES', event.text):
            database.insert_data('bag_words', 'LITRES', event.text)

