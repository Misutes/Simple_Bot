import Text as t
import random
import keyboard
from keyboard import new_keyboard

book_challenge_info_dict = {}
accepted = 0
performed = 0


# отправляет вступительное сообщение с фото книги
def send_preview(session, event):
    owner_id = '-193464895'
    media_id = '457239018'
    photo = f'photo{owner_id}_{media_id}'
    session.method('messages.send',
                   {'user_id': event.user_id, 'attachment': photo, 'random_id': random.randint(0, 10 ** 10)})


# отправляет вступительное сообщение с описанием челленджа
def start_challenge(session, event, send_func, empty, user_name):
    global book_challenge_info_dict, accepted, performed
    send_preview(session, event)
    # описание книги
    send_func(t.description, new_keyboard(keyboard.challenge_book_link_keyboard))
    send_func(f'Вызов приняли: {accepted} человек'
              f'\nА выполнили: {performed} человек', None)
    send_func(empty, new_keyboard(keyboard.book_challenge_keyboard))


# меню челленджа
def book_challenge(message, send_func, empty, user_name, user_check_dict):
    global book_challenge_info_dict, accepted, performed
    challenge = True
    for word in message:
        # меняет статус пользователя и отправляет основную клавиатуру
        if word == 'уйти':
            challenge = False
            user_check_dict[info['id']]['challenge'] = 0
            send_func(info['first_name'] + t.suggestion, new_keyboard(keyboard.function_keyboard))
        # если пользователь решил принять вызов
        elif word == 'принять':
            # создается его статус-словарь для этого челленджа
            book_challenge_info_dict.setdefault(info['id'], [info['first_name'], info['last_name'], 0, 0])
            print(book_challenge_info_dict)
            # если челлендж не был принят
            if book_challenge_info_dict[info['id']][2] == 0:
                print('challenge accepted')
                book_challenge_info_dict[info['id']][2] = 1
                accepted += 1
                send_func(t.adoption, None)
            # если челлендж был принят
            else:
                name = info['first_name']
                send_func((name + t.inside), None)
        # если пользователь хочет отметить книгу прочитанной
        elif word == 'прочитана!':
            # проверка, был ли принят челлендж
            if book_challenge_info_dict[info['id']][2] == 1:
                # проверка, не отмечена ли книга прочитанной
                if book_challenge_info_dict[info['id']][3] == 0:
                    print('book is finished')
                    book_challenge_info_dict[info['id']][3] = 1
                    performed += 1
                    send_func(t.finish, None)
                # если книга уже отмечена прочитаной
                else:
                    send_func(t.finish_repetition, None)
            # если челлендж не принят
            else:
                send_func(t.not_accept, None)
    # отправляет меню челленджа
    if challenge:
        send_func(empty, new_keyboard(keyboard.book_challenge_keyboard))
