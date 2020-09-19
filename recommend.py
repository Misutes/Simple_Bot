import random

import keyboard as kb

quit_ = ['уйти']
novelty_ = ['новинки']
fantastic = ['фантастика']
japan = ['япония']
detective = ['детективы', 'детектив']
adult = ['подростковая', 'детей']
recommendation = ['климент', 'посоветуйте']
parting = ['спасибо']


def recommend(event, class_, message, sm, ssm, database, media_1, media_2, media_3):
    miss_word = 0
    user_name = str(database.find_data('users', 'NAME_', 'ID', event.user_id)[0])

    def random_post(text, posts):
        sm(message=text)
        ssm('wall', class_.get_text('group_id'), random.choice(posts))

    for word in message:

        if word in quit_:
            database.update_data('users', 'RECOMMENDATION', 0, event.user_id)
            sm(user_name + class_.get_text('quit_'), kb.main_menu)
            sm(class_.get_text('staff_connect'), kb.staff_call)

        elif word in novelty_:
            sm(class_.get_text('novelty_bookshelf'), kb.novelty_bookshelf)

        elif word in fantastic:
            random_post(class_.get_text('fantastic'), class_.get_text('fantastic_literature'))

        elif word in japan:
            random_post(class_.get_text('japan'), class_.get_text('japan_literature'))

        elif word in detective:
            random_post(class_.get_text('detective'), class_.get_text('detective_literature'))

        elif word in adult:
            ssm(*media_3)
            sm(class_.get_text('adult_bookshelf'), kb.adult_bookshelf)

        elif word in recommendation:
            ssm(*media_1)
            sm(class_.get_text('advice_description'), kb.advice_book)

        elif word in parting:
            ssm(*media_2)

        else:
            miss_word += 1

    if miss_word > len(message) - 1:
        sm(message=class_.get_text('bookshelf_exit'))
        if not database.find_data('bag_words', 'RECOMMENDATION', 'RECOMMENDATION', event.text):
            database.insert_data('bag_words', 'RECOMMENDATION', event.text)
