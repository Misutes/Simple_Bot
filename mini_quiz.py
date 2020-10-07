import time

import keyboard as kb

quit_ = ['уйти']


def quiz(event, class_,  message, sm, ssm, database, media):
    user_name = str(database.find_data('users', 'NAME_', 'ID', event.user_id)[0])

    def media_question(i, k):
        sm(message=class_.get_data('quiz_right') + class_.get_data('answer')[position])
        ssm(*media[i][k])
        sm(message=class_.get_data('q_a')[position + 1][0])

    def media_answer(i, k):
        sm(message=class_.get_data('quiz_right') + class_.get_data('answer')[position])
        ssm(*media[i][k])
        sm(message=class_.get_data('q_a')[position + 1][0])

    for word in message:
        if word in quit_:
            database.update_data('users', 'QUIZ', 0, event.user_id)
            sm(user_name + class_.get_data('quit_'), kb.main_menu)
            sm(class_.get_data('staff_connect'), kb.staff_call)
            return

    position = database.find_data('quiz', 'QUESTION', 'ID', event.user_id)[0]-1
    if str(message[0]) == str(class_.get_data('q_a')[position][1]):
        database.update_data('quiz', 'CORR_ANS', 'CORR_ANS + 1', event.user_id)

    if position + 1 < len((class_.get_data('q_a'))):
        database.update_data('quiz', 'QUESTION', 'QUESTION + 1', event.user_id)
        if position == 4:
            media_question(0, 0)
        elif position == 5:
            media_answer(0, 1)
        elif position == 6:
            media_question(1, 0)
        elif position == 7:
            media_answer(1, 1)
        else:
            sm(message=class_.get_data('quiz_right') + class_.get_data('answer')[position])
            sm(message=class_.get_data('q_a')[position + 1][0])

    else:
        end = time.time()
        start = int(database.find_data('quiz', 'TIME_', 'ID', event.user_id)[0])
        database.update_data('quiz', 'TIME_', end-start, event.user_id)
        database.update_data('users', 'QUIZ', 0, event.user_id)

        count = str(database.count_data('quiz', 'QUESTION', 10)[0])
        sm(message=user_name + class_.get_data('quiz_end_text'))
        sm(message=class_.get_data('quiz_count') + count)

        sm(class_.get_data('quit_2'), kb.main_menu)
        sm(class_.get_data('staff_connect'), kb.staff_call)

