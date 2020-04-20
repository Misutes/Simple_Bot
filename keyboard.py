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
            [get_text_buttons(label='Написать кое-что', color='positive')]
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