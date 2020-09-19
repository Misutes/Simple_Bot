from classes import Reply

admin_ids = [122226430]
command_list = ['терминал']


def terminal(session, event, class_, database, ssm, media):
    admin_reply = Reply(session, event)
    if database.check_position('users', 'PAUSE', 0, event.user_id):
        database.update_data('users', 'PAUSE', 1, event.user_id)
    elif 'бот' == event.text.lower():
        database.update_data('users', 'PAUSE', 0, event.user_id)
        admin_reply.em(class_.get_text('edit_message'))
        ssm(*media)
