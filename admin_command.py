import Text as t

# список id  администраторов
admin_id_list = [122226430]
# список всех команд администрации
command_list = ['терминал']


# редактирование сообщения
def bot_edit_message(session, event, message):
    session.method('messages.edit', {'peer_id': event.user_id, 'message_id': event.message_id,
                                     'message': message})


# подключение бота в работу
def bot_return(session, event, database, special, args):
    # если администратор написал, бот отключится
    if database.update_data('users', 'PAUSE', 0, event.user_id):
        database.update_data('users', 'PAUSE', 1, event.user_id)
    # позволяет закончить общение, если написать "бот"
    if 'бот' == event.text.lower():
        database.update_data('users', 'PAUSE', 0, event.user_id)
        bot_edit_message(session, event, t.edit)
        special(*args)

# терминал управления ботом
def terminal(message, message_function):
    pass
