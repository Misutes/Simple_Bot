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
        [get_text_buttons(label='Режим работы/Адрес', color='positive')],
        [get_text_buttons(label='Продлить книги', color='positive')],
        [get_text_buttons(label='Афиша', color='positive')],
        [get_text_buttons(label='Что почитать?', color='positive'), get_text_buttons(label='ЛитРес', color='positive')],
        [get_text_buttons(label='Видео-лекции', color='positive'),
         get_text_buttons(label='Экскурсии', color='positive')],
        [get_text_buttons(label='Цитата дня', color='primary')]
        # [get_text_buttons(label='Книжный вызов', color='primary')]
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
first_lecture_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Культура Ленинграда 45-65 гг',
                          'https://vk.com/timiriazevka?z=video-43349586_456239075%2F23db0421e4fd2913ef%2Fpl_wall_-43349586')],
        [get_link_buttons('Поэма «Бахчисарайский фонтан»',
                          'https://vk.com/timiriazevka?z=video-43349586_456239080%2F4aa3766124e103fb87%2Fpl_wall_-43349586')],
        [get_link_buttons('Арт-мэм',
                          'https://vk.com/wall-43349586_7554?z=video-43349586_456239081%2F56e2be2df1ab037431%2Fpl_post_-43349586_7554')],
        [get_link_buttons('Советский балет в Японии',
                          'https://vk.com/wall-43349586_7683?z=video-43349586_456239084%2Fc723d97d7a51206b28%2Fpl_post_-43349586_7683')]

    ]
}

# второй лектор
second_lecture_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Бродский и Петербург',
                          'https://vk.com/timiriazevka?z=video-43349586_456239088%2F1ca892e1970b5c468c%2Fpl_wall_-43349586')],

    ]
}

# третий лектор
third_lecture_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Основатели японского буддизма',
                          'https://vk.com/wall-43349586_7661?z=video-43349586_456239083%2F872fb2748326b1a84b%2Fpl_post_-43349586_7661')],

    ]
}

# четвертый лектор
fourth_lecture_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Три имени библиотеки',
                          'https://vk.com/wall-43349586_7705?z=video-43349586_456239085%2Fe45ea703b650827f13%2Fpl_post_-43349586_7705')],

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
recommendation_keyboard = {
    "inline": True,
    "buttons": [
        [get_text_buttons(label='Новинки', color='positive')],
        [get_text_buttons(label='Фантастика', color='positive'), get_text_buttons(label='Япония', color='positive')],
        [get_text_buttons(label='Климент рекомендует!', color='primary')],
        [get_text_buttons(label='Уйти', color='positive')]

    ]
}

# ссылка на "Фантастику"
fantastic_link = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Фантастика',
                          'https://vk.com/wall-43349586?q=%23МирФантастики')],

    ]
}
# ссылка на "Японию"
japan_link = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Япония',
                          'https://vk.com/timiriazevka/FromLibToJapan')],

    ]
}
# ссылка на рекомендуемую книгу
recommendation_link = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Читать по ссылке',
                          'https://www.litres.ru/edit-eva-eger/vybor/')],

    ]
}

# Афиша
poster_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Афиша',
                          'https://vk.cc/auUdHT')],

    ]
}

# экскурсии
excursion_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Часть 1', 'https://vk.cc/auXvnb'), get_link_buttons('Часть 2', 'https://vk.cc/auXvFq')],
        [get_link_buttons('Часть 3', 'https://vk.cc/auXvHG'), get_link_buttons('Часть 4', 'https://vk.cc/auXvJK')],
        [get_link_buttons('Часть 5', 'https://vk.cc/auXvLF'), get_link_buttons('Часть 6', 'https://vk.cc/auXvPG')],
        [get_link_buttons('Часть 7', 'https://vk.cc/auXvTd'), get_link_buttons('Часть 8', 'https://vk.cc/auXvUr')],
        [get_link_buttons('Часть 9', 'https://vk.cc/auXvVL'), get_link_buttons('Часть 10', 'https://vk.cc/auXvYA')]

    ]
}
