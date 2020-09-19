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
def json_keyboard(keyboard):
    keyboard = str(json.dumps(keyboard, ensure_ascii=False))
    return keyboard


# основное меню
main_menu = json_keyboard({
    "inline": True,
    "buttons": [
        [get_text_buttons(label='Режим работы/Адрес', color='positive')],
        [get_text_buttons(label='Продлить книги', color='positive')],
        [get_text_buttons(label='Мероприятия', color='positive')],
        [get_text_buttons(label='Что почитать?', color='positive'), get_text_buttons(label='ЛитРес', color='positive')],
        [get_text_buttons(label='Видео-лекции', color='positive'),
         get_text_buttons(label='Экскурсии', color='positive')],
        [get_text_buttons(label='Цитата дня', color='primary')]
        # [get_text_buttons(label='Книжный вызов', color='primary')]
    ]
})

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
renewal_book = json_keyboard({
    "inline": True,
    "buttons": [
        [
            get_link_buttons('Продление книги', 'https://vk.com/app6013442_-43349586?form_id=1#form_id=1')
        ]
    ]
})

# связь с сотрудником
staff_call = json_keyboard({
    "inline": True,
    "buttons": [
        [get_text_buttons(label='Связаться с библиотекарем', color='positive')],
        [get_link_buttons('Сотрудничество', 'https://docs.google.com/forms/d/e/1FAIpQLSegQmN6POvXBMBUY0Z0KNxgSpn02CVK854IOOmZd4ysKwe4uQ/viewform')]
    ]
})

geo_position = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Показать на карте', 'https://go.2gis.com/dglte')]
    ]
})
# первый лектор
first_lecturer = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Культура Ленинграда 45-65 гг',
                          'https://vk.com/timiriazevka?z=video-43349586_456239075%2F23db0421e4fd2913ef%2Fpl_wall_-43349586')],
        [get_link_buttons('Поэма «Бахчисарайский фонтан»',
                          'https://vk.com/timiriazevka?z=video-43349586_456239080%2F4aa3766124e103fb87%2Fpl_wall_-43349586')],
        [get_link_buttons('Арт-мэм',
                          'https://vk.com/wall-43349586_7554?z=video-43349586_456239081%2F56e2be2df1ab037431%2Fpl_post_-43349586_7554')],
        [get_link_buttons('Советский балет в Японии',
                          'https://vk.com/wall-43349586_7683?z=video-43349586_456239084%2Fc723d97d7a51206b28%2Fpl_post_-43349586_7683')],
        [get_link_buttons('"Честное слово" Л.Пантелеев',
                          'https://vk.com/video-43349586_456239091?list=338bed4e0923fe988b')],
        [get_link_buttons('Балет в советской культуре',
                          'https://vk.com/timiriazevka?z=video-43349586_456239092%2F6b46df7aaf126d0333%2Fpl_wall_-43349586')],


    ]
})

first_lecturer_two = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Советская школьная повседневность',
                          'https://vk.com/timiriazevka?z=video-43349586_456239103%2Fa809bef509fb8dd504%2Fpl_wall_-43349586')]
    ]
})


# второй лектор
second_lecturer = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Бродский и Петербург',
                          'https://vk.com/timiriazevka?z=video-43349586_456239088%2F1ca892e1970b5c468c%2Fpl_wall_-43349586')],

    ]
})

# третий лектор
third_lecturer = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Основатели японского буддизма',
                          'https://vk.com/wall-43349586_7661?z=video-43349586_456239083%2F872fb2748326b1a84b%2Fpl_post_-43349586_7661')],

    ]
})

# четвертый лектор
fourth_lecturer = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Три имени библиотеки',
                          'https://vk.com/wall-43349586_7705?z=video-43349586_456239085%2Fe45ea703b650827f13%2Fpl_post_-43349586_7705')],

    ]
})

# четвертый лектор
fifth_lecturer = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('«История старой квартиры»',
                          'https://vk.com/timiriazevka?z=video-43349586_456239097%2F6a93e2028141fc0e99%2Fpl_wall_-43349586')],

    ]
})

# книга для "Книжного вызова"
challenge_book_link_keyboard = {
    "inline": True,
    "buttons": [
        [get_link_buttons('Название книги',
                          'https://www.litres.ru/')],

    ]
}

# меню "ЛитРес"
litres_menu = json_keyboard({
    "inline": True,
    "buttons": [
        [get_text_buttons(label='Что это такое?', color='positive')],
        [get_text_buttons(label='Как получить доступ?', color='positive')],
        [get_link_buttons('Правила пользования',
                          'https://vk.com/@timiriazevka-pravila-polzovaniya-litres')],
        [get_text_buttons(label='Уйти', color='primary')],

    ]
})

# получения доступа к "ЛитРес"
get_litres = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Получить доступ',
                          'https://vk.com/app6013442_-43349586?form_id=2#form_id=2')],

    ]
})

bookshelf_menu = json_keyboard({
    "inline": True,
    "buttons": [
        [get_text_buttons(label='Новинки', color='positive')],
        [get_text_buttons(label='Фантастика', color='positive'), get_text_buttons(label='Япония', color='positive')],
        [get_text_buttons(label='Детективы', color='positive'), get_text_buttons(label='Подростковая', color='positive')],
        [get_text_buttons(label='Климент рекомендует!', color='primary')],
        [get_text_buttons(label='Уйти', color='positive')]

    ]
})

# ссылка на рекомендуемую книгу
advice_book = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Забронировать',
                          'https://lermontovka-spb.ru/services/booking/')],

    ]
})

# ссылка на новинки
novelty_bookshelf = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Заглянуть на полку',
                          'https://www.livelib.ru/bookshelf/1656367-knizhnye-novinki-sentyabroktyabr-2020/listview/smalltiles')],

    ]
})

# ссылка на подростковую
adult_bookshelf = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Заглянуть на полку',
                          'https://www.livelib.ru/bookshelf/1640287-knigi-dlya-podrostkov/listview/smalltiles')],

    ]
})

# Афиша
poster = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Афиша',
                          'https://vk.cc/auUdHT')],
        [get_link_buttons('Записаться на мероприятие',
                          'https://vk.cc/azEMqA')]

    ]
})

# экскурсии
excursion = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Часть 1', 'https://vk.cc/auXvnb'), get_link_buttons('Часть 2', 'https://vk.cc/auXvFq')],
        [get_link_buttons('Часть 3', 'https://vk.cc/auXvHG'), get_link_buttons('Часть 4', 'https://vk.cc/auXvJK')],
        [get_link_buttons('Часть 5', 'https://vk.cc/auXvLF'), get_link_buttons('Часть 6', 'https://vk.cc/auXvPG')],
        [get_link_buttons('Часть 7', 'https://vk.cc/auXvTd'), get_link_buttons('Часть 8', 'https://vk.cc/auXvUr')],
        [get_link_buttons('Часть 9', 'https://vk.cc/auXvVL'), get_link_buttons('Часть 10', 'https://vk.cc/auXvYA')]

    ]
})

excursion_two = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Часть 11', 'https://vk.cc/avBjl2')]

    ]
})

excursion_three = json_keyboard({
    "inline": True,
    "buttons": [
        [get_link_buttons('Часть 1', 'https://vk.cc/avKJNB'), get_link_buttons('Часть 2', 'https://vk.cc/aycMQb')],
        [get_link_buttons('Часть 3', 'https://vk.cc/aycNif'), get_link_buttons('Часть 4', 'https://vk.cc/aycNW8')],
        [get_link_buttons('Часть 5', 'https://vk.cc/aycO5o'), get_link_buttons('Часть 6', 'https://vk.cc/aycOg4')],
    ]
})
