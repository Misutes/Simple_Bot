
import random
import keyboard
from keyboard import new_keyboard

book_challenge_info_dict = {}
challenge_user_list = []
accepted = 0
performed = 0


def send_preview(session, event):
    owner_id = '-193464895'
    media_id = '457239018'
    photo = f'photo{owner_id}_{media_id}'
    session.method('messages.send',
                   {'user_id': event.user_id, 'attachment': photo, 'random_id': random.randint(0, 10 ** 10)})


challenge_text = 'В книге автор раскрывает секреты орального секса и объясняет, ' \
                 'почему он имеет огромное значение для построения прочных отношений с мужчиной.'


def start_challenge(session, event, mess_func, empty, info):
    global book_challenge_info_dict, challenge_user_list, accepted, performed
    if info['id'] not in book_challenge_info_dict.keys():
        book_challenge_info_dict.setdefault(info['id'], [info['first_name'], info['last_name'], 0, 0])
    send_preview(session, event)
    mess_func(challenge_text, new_keyboard(keyboard.challenge_book_link_keyboard))
    mess_func(f'Сейчас вызов приняли: {accepted} человек\n А выполнили: {performed} человек', None)
    mess_func(empty, new_keyboard(keyboard.book_chal_keyboard))


def book_challenge(message, mess_func, empty, info, quit):
    global book_challenge_info_dict, challenge_user_list, accepted, performed
    challenge = True
    for word in message:
        if word == 'уйти':
            challenge = False
            quit[info['id']] = 0
            mess_func(info['first_name'] + ', Климент Аркадьевич может предложить',
                      new_keyboard(keyboard.function_keyboard))
        elif word == 'посмотреть':
            if len(challenge_user_list):
                help_string = ''
                for element in challenge_user_list:
                    help_string += element
                    help_string += ', '
                mess_func(help_string, None)
            else:
                mess_func('Пока никто не принял вызов :(', None)
        elif word == 'принять':
            if book_challenge_info_dict[info['id']][2] == 0:
                print('challenge accepted')
                challenge_user_list.append(str(info['first_name']) + ' ' + str(info['last_name']))
                book_challenge_info_dict[info['id']][2] = 1
                accepted += 1
                mess_func('Поздравляем с принятием челленджа!', None)
            else:
                name = info['first_name']
                mess_func(f'{name}, Вы уже в челлендже!', None)
        elif word == 'прочитана!':
            if book_challenge_info_dict[info['id']][2] == 1:
                if book_challenge_info_dict[info['id']][3] == 0:
                    print('book is finished')
                    book_challenge_info_dict[info['id']][3] = 1
                    performed += 1
                    mess_func('Поздравляем с завершением челленджа!', None)
                else:
                    mess_func('Вы уже отметили эту книгу как прочитанную.', None)
            else:
                mess_func('Вы еще не приняли вызов!', None)

    if challenge:
        mess_func(empty, new_keyboard(keyboard.book_chal_keyboard))
