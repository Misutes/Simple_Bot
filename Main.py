from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api

token = '79eee7ae818b1db0d38b95f8911b1576e3d3a325c3622f6feaead4f3de1b09cdb0285cc9ac8308fb471f2'
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

list_of_greeting = ['привет', 'здравствуйте', 'добрый утро', 'добрый день', 'добрый вечер',
                    'привет.', 'здравствуйте.', 'добрый утро.', 'добрый день.', 'добрый вечер.',
                    'привет!', 'здравствуйте!', 'добрый утро!', 'добрый день!', 'добрый вечер!']

hello_message = ', привет! Я официальный бот-помощник библиотеки им. К.А.Тимирязева. \n' \
                'И вот что я умею: \n' \
                '1. Могу помочь Вам продлить книгу \n'

missunderstanding_message = 'Я из другой эпохи, эти вопросы не ко мне!'


def message(message):
    vk_session.method('messages.send', {'user_id': event.user_id, 'message': message, "random_id": 0})


while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_message = event.text
            user_message = user_message.lower()
            user_info = session_api.users.get(user_ids=event.user_id)
            if user_message in list_of_greeting:
                message(user_info[0]['first_name'] + hello_message)
            elif user_message == '1':
                message('вот ссылочка: \n https://vk.com/app6013442_-43349586#form_id=1')
            else:
                pass
