import time

import Text as t
import keyboard
from keyboard import new_keyboard

quit_ = ['уйти']


def quiz(event, message, sm, ssm, database, media):
    user_name = str(database.find_data('users', 'NAME_', 'ID', event.user_id)[0])

    def media_question(i, k):
        sm(message=t.quiz_right + t.answer[position])
        ssm(*media[i][k])
        sm(message=t.q_a[position + 1][0])

    def media_answer(i, k):
        sm(message=t.quiz_right + t.answer[position])
        ssm(*media[i][k])
        sm(message=t.q_a[position + 1][0])

    for word in message:
        if word in quit_:
            database.update_data('users', 'QUIZ', 0, event.user_id)
            sm(user_name + t.quit, new_keyboard(keyboard.function_keyboard))
            sm(t.connection, new_keyboard(keyboard.call_staff))
            return

    position = database.find_data('quiz', 'QUESTION', 'ID', event.user_id)[0]-1
    if str(message[0]) == str(t.q_a[position][1]):
        database.update_data('quiz', 'CORR_ANS', 'CORR_ANS + 1', event.user_id)

    if position + 1 < len(t.q_a):
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
            sm(message=t.quiz_right + t.answer[position])
            sm(message=t.q_a[position + 1][0])

    else:
        end = time.time()
        start = int(database.find_data('quiz', 'TIME_', 'ID', event.user_id)[0])
        database.update_data('quiz', 'TIME_', end-start, event.user_id)
        database.update_data('users', 'QUIZ', 0, event.user_id)

        count = str(database.count_data('quiz', 'QUESTION', 10)[0])
        sm(message=user_name + t.quiz_end_text)
        sm(message=t.quiz_count + count)

        sm(t.quit_2, new_keyboard(keyboard.function_keyboard))
        sm(t.connection, new_keyboard(keyboard.call_staff))

