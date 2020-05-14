admin_id_list = [122226430]
command_list = ['терминал']


def bot_edit_message(session, event, message):
    session.method('messages.edit', {'peer_id': event.user_id, 'message_id': event.message_id,
                                     'message': message})


message = 'Спасибо за обращение!'


def bot_return(session, event, dict):
    if 'бот' == event.text.lower():
        dict[event.user_id] = 0
        bot_edit_message(session, event, message)


def terminal(message, message_function):
    pass
