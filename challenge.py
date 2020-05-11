from vk_api.longpoll import VkEventType

import keyboard
from keyboard import new_keyboard

book_chal = {}
challenge_user_list = []
accepted = 0
performed = 0
def start_challenge(mess_func, empty, info):
    global book_chal, challenge_user_list, accepted, performed
    if info['id'] not in book_chal.keys():
        book_chal.setdefault(info['id'], [info['first_name'], info['last_name'], 0, 0])
    mess_func('картинка', None)
    mess_func('название, описание и ссылка', None)
    mess_func(f'Сейчас вызов приняли: {accepted} человек', None)
    mess_func(f'А выполнили: {performed} человек', None)
    mess_func(empty, new_keyboard(keyboard.book_chal_keyboard))

def book_challenge(event, mess_func, empty, mess_trans_func, info, quit):
    global book_chal, challenge_user_list, accepted, performed
    challenge = True
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            mess = mess_trans_func(event.text)
            for x in mess:
                if x == 'уйти':
                    challenge = False
                    quit[info['id']] = 0
                    mess_func(info['first_name'] + ', Климент Аркадьевич может предложить', new_keyboard(keyboard.function_keyboard))
                elif x == 'посмотреть':
                    if len(challenge_user_list):
                        help_string = ''
                        for element in challenge_user_list:
                            help_string += element
                            help_string += ', '
                        mess_func(help_string, None)
                    else:
                        mess_func('Пока никто не принял вызов :(', None)
                elif x == 'прочитана!':
                    if book_chal[info['id']][3] == 0:
                        print('book is finished')
                        book_chal[info['id']][3] = 1
                        performed += 1
                        mess_func('Поздравляем с заверщением челленджа!', None)
                    else:
                        mess_func('Вы уже отметили эту книгу как прочитанную.', None)
                elif x == 'принять':
                    if book_chal[info['id']][2] == 0:
                        print('challenge accepted')
                        challenge_user_list.append(str(info['first_name']) + ' ' + str(info['last_name']))
                        book_chal[info['id']][2] = 1
                        accepted += 1
                        mess_func('Поздравляем с принятием челленджа!', None)
                    else:
                        name = info['first_name']
                        mess_func(f'{name}, Вы уже в челлендже!', None)

            if challenge:
                mess_func(empty, new_keyboard(keyboard.book_chal_keyboard))

