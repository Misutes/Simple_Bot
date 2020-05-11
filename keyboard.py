import json


def get_text_buttons(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


def get_link_buttons(label, link):
    return {
        "action": {
            "type": "open_link",
            "label": label,
            "link": link
        }
    }


def new_keyboard(keyboard):
    keyboard = str(json.dumps(keyboard, ensure_ascii=False))
    return keyboard


function_keyboard ={
    "inline": True,
    "buttons": [
            [get_text_buttons(label='Продление книги', color='positive')],
            [get_text_buttons(label='Видео-лекции', color='positive')],
            [get_text_buttons(label='Рекомендация', color='primary')],
            [get_text_buttons(label='Книжный вызов', color='primary')]
    ]
}

book_chal_keyboard ={
    "inline": True,
    "buttons": [
        [get_text_buttons(label='Принять вызов!', color='positive')],
        [get_text_buttons(label='Книга прочитана!', color='primary')],
        [get_text_buttons(label='Посмотреть список участников', color='primary')],
        [get_text_buttons(label='Уйти', color='primary')],
    ]
}

link_keyboard = {
        "inline": True,
        "buttons": [
            [
                get_link_buttons('Продление книги',
                                 'https://vk.com/app6013442_-43349586?form_id=1#form_id=1')
            ]
        ]
    }

call_staff = {
    "inline": True,
    "buttons": [
        [
            get_text_buttons(label='Связаться с сотрудником', color='positive')
        ]
    ]
}

recommend_link_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Модели сезона весна 45г.',
                          'https://vk.com/timiriazevka?z=video-43349586_456239079%2F4a35bcaaa3601a6627%2Fpl_wall_-43349586')],

    ]
}

olga_link_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Культура Ленинграда 45-65 гг',
                             'https://vk.com/timiriazevka?z=video-43349586_456239075%2F23db0421e4fd2913ef%2Fpl_wall_-43349586')],
        [get_link_buttons('Поэма «Бахчисарайский фонтан»',
                          'https://vk.com/timiriazevka?z=video-43349586_456239080%2F4aa3766124e103fb87%2Fpl_wall_-43349586')]

    ]
}

unknown_link_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('???',
                          'https://vk.com/timiriazevka?z=video-43349586_456239075%2F23db0421e4fd2913ef%2Fpl_wall_-43349586')],

    ]
}
