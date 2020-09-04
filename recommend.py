import random

import Text as t
import keyboard
from keyboard import new_keyboard

quit_ = ['уйти']
novelty_ = ['новинки']
fantastic = ['фантастика']
japan = ['япония']
detective = ['детективы', 'детектив']
adult = ['подростковая', 'детей']
recommendation = ['климент', 'посоветуйте']


def recommend(event, message, sm, ssm, database, media_1, media_2):
    miss_word = 0
    user_name = str(database.find_data('users', 'NAME_', 'ID', event.user_id)[0])

    def random_post(text, posts):
        sm(message=text)
        ssm('wall', t.group_id, random.choice(posts))

    for word in message:

        if word in quit_:
            database.update_data('users', 'RECOMMENDATION', 0, event.user_id)
            sm(user_name + t.quit, new_keyboard(keyboard.function_keyboard))
            sm(t.connection, new_keyboard(keyboard.call_staff))

        elif word in novelty_:
            sm(t.novelty, new_keyboard(keyboard.novelty_bookshelf_link))

        elif word in fantastic:
            random_post(t.fantastic_literature, t.fantastic)

        elif word in japan:
            random_post(t.japan_literature, t.japan)

        elif word in detective:
            random_post(t.detective_literature, t.detective)

        elif word == 'подростковая':
            sm(t.teen, new_keyboard(keyboard.teen_bookshelf_link))

        elif word in recommendation:
            ssm(*media_1)
            sm(t.recommendation_description, new_keyboard(keyboard.recommendation_link))

        elif word in t.parting:
            ssm(*media_2)

        else:
            miss_word += 1

    if miss_word > len(message)-1:
        sm(message=t.help_recommendation)
        if not database.find_data('bag_words', 'RECOMMENDATION', 'RECOMMENDATION', event.text):
            database.insert_data('bag_words', 'RECOMMENDATION', event.text)

