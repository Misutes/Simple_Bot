import keyboard as kb

quit_ = ['уйти']
what_read = ['что']
access = ['как']
connection_list = ['связаться']
parting = ['спасибо']


def litres(event, class_, message, sm, ssm, database, media):
    miss_word = 0
    user_name = str(database.find_data('users', 'NAME_', 'ID', event.user_id)[0])
    for word in message:

        if word in quit_:
            database.update_data('users', 'LITRES', 0, event.user_id)
            sm(user_name + class_.get_data('quit_'), kb.main_menu)
            sm(class_.get_data('staff_connect'), kb.staff_call)

        elif word in what_read:
            sm(message=class_.get_data('litres_description'))

        elif word in access:
            sm(class_.get_data('litres_access'), kb.get_litres)

        elif word in parting:
            ssm(media)

        elif word in connection_list:
            database.update_data('users', 'LITRES', 0, event.user_id)
            database.update_data('users', 'PAUSE', 1, event.user_id)

        else:
            miss_word += 1

    if miss_word > len(message)-1:
        sm(message=class_.get_data('litres_exit'))
        if not database.find_data('bag_words', 'LITRES', 'LITRES', event.text):
            database.insert_data('bag_words', 'LITRES', event.text)

