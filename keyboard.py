import json


# создает обычную кнопку
def get_text_buttons(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


# создает ссылку
def get_link_buttons(label, link):
    return {
        "action": {
            "type": "open_link",
            "label": label,
            "link": link
        }
    }


# создает json клавиатуру
def new_keyboard(keyboard):
    keyboard = str(json.dumps(keyboard, ensure_ascii=False))
    return keyboard


# основное меню
function_keyboard = {
    "inline": True,
    "buttons": [
        [get_text_buttons(label='Продление книги', color='positive')],
        [get_text_buttons(label='Режим работы/Адрес', color='positive')],
        [get_text_buttons(label='ЛитРес', color='positive')],
        [get_text_buttons(label='Видео-лекции', color='positive')],
        [get_text_buttons(label='Рекомендация', color='positive')],
        [get_text_buttons(label='Книжный вызов', color='primary')]
    ]
}

# меню "Книжного вызова"
book_challenge_keyboard = {
    "inline": True,
    "buttons": [
        [get_text_buttons(label='Принять вызов!', color='positive')],
        [get_text_buttons(label='Книга прочитана!', color='primary')],
        [get_text_buttons(label='Уйти', color='primary')],
    ]
}

# ссылка для пробления книги
link_keyboard = {
    "inline": True,
    "buttons": [
        [
            get_link_buttons('Продление книги',
                             'https://vk.com/app6013442_-43349586?form_id=1#form_id=1')
        ]
    ]
}

# связь с сотрудником
call_staff = {
    "inline": True,
    "buttons": [
        [get_text_buttons(label='Связаться с библиотекарем', color='positive')]
    ]
}

# первый лектор
olga_link_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Культура Ленинграда 45-65 гг',
                          'https://vk.com/timiriazevka?z=video-43349586_456239075%2F23db0421e4fd2913ef%2Fpl_wall_-43349586')],
        [get_link_buttons('Поэма «Бахчисарайский фонтан»',
                          'https://vk.com/timiriazevka?z=video-43349586_456239080%2F4aa3766124e103fb87%2Fpl_wall_-43349586')]

    ]
}

# второй лектор
unknown_link_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('???',
                          'https://vk.com/timiriazevka?z=video-43349586_456239075%2F23db0421e4fd2913ef%2Fpl_wall_-43349586')],

    ]
}

# книга для "Книжного вызова"
challenge_book_link_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Название книги',
                          'https://www.litres.ru/')],

    ]
}

# меню "ЛитРес"
litres_keyboard = {
    "inline": True,
    "buttons": [
        [get_text_buttons(label='Что это такое?', color='positive')],
        [get_text_buttons(label='Как получить доступ?', color='positive')],
        [get_link_buttons('Правила пользования',
                          'https://vk.com/@timiriazevka-pravila-polzovaniya-litres')],
        [get_text_buttons(label='Уйти', color='primary')],

    ]
}

# получения доступа к "ЛитРес"
access_link = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Получить доступ',
                          'https://vk.com/app6013442_-43349586?form_id=2#form_id=2')],

    ]
}
