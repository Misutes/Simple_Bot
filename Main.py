from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api, keyboard, Text
from keyboard import new_keyboard



token = '79eee7ae818b1db0d38b95f8911b1576e3d3a325c3622f6feaead4f3de1b09cdb0285cc9ac8308fb471f2'
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

user_list = []


def message(message, keyboard):
    vk_session.method('messages.send', {
        'user_id': event.user_id,
        'message': message,
        "random_id": 0,
        "keyboard": keyboard
    })


while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_message = event.text
            user_message = user_message.lower()
            user_info = session_api.users.get(user_ids=event.user_id)
            user_info = user_info[0]
            if user_message in Text.list_of_greeting:
                if user_info['id'] not in user_list:
                    user_list.append(user_info['id'])
                    message(user_info['first_name'] + Text.hello_message, new_keyboard(keyboard.function_keyboard))
                else:
                    message(user_info['first_name'] + str(', категорически приветствую! Напомниаю, что я могу: '),
                            new_keyboard(keyboard.function_keyboard))
            elif user_message.lower() == 'продление книги':
                message(user_info['first_name'] + str(' , Вы можете сделать это здесь'),
                        new_keyboard(keyboard.link_keyboard))
            elif user_message.lower() == 'написать кое-что':
                message(user_info['first_name'] + str(', я же умненький?'),
                        None)