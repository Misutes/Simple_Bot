import random

import Text as t
import keyboard as kb

quit_ = ['уйти']
novelty_ = ['новинки']
fantastic = ['фантастика']
japan = ['япония']
detective = ['детективы', 'детектив']
adult = ['подростковая', 'детей']
recommendation = ['климент', 'посоветуйте']
parting = ['спасибо']

def recommend(event, message, sm, ssm, database, media_1, media_2, media_3):
    miss_word = 0
    user_name = str(database.find_data('users', 'NAME_', 'ID', event.user_id)[0])

    def random_post(text, posts):
        sm(message=text)
        ssm('wall', t.group_id, random.choice(posts))

    for word in message:

        if word in quit_:
            database.update_data('users', 'RECOMMENDATION', 0, event.user_id)
            sm(user_name + t.quit_, kb.main_menu)
            sm(t.staff_connect, kb.staff_call)

        elif word in novelty_:
            sm(t.novelty_bookshelf, kb.novelty_bookshelf)

        elif word in fantastic:
            random_post(t.fantastic, t.fantastic_literature)

        elif word in japan:
            random_post(t.japan, t.japan_literature)

        elif word in detective:
            random_post(t.detective, t.detective_literature)

        elif word in adult:
            ssm(*media_3)
            sm(t.adult_bookshelf, kb.adult_bookshelf)

        elif word in recommendation:
            ssm(*media_1)
            sm(t.advice_description, kb.advice_book)

        elif word in parting:
            ssm(*media_2)

        else:
            miss_word += 1

    if miss_word > len(message)-1:
        sm(message=t.bookshelf_exit)
        if not database.find_data('bag_words', 'RECOMMENDATION', 'RECOMMENDATION', event.text):
            database.insert_data('bag_words', 'RECOMMENDATION', event.text)

