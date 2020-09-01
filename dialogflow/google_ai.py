import json

import apiai

token = '036101f6da9948318ac5f645a4eb4782'


def response(string):
    dialog_session = apiai.ApiAI(token).text_request()
    dialog_session.lang = 'ru'
    dialog_session.session_id = 'simple_bot'
    dialog_session.query = string
    try:
        response_json = json.loads(dialog_session.getresponse().read().decode('utf-8'))
        response = response_json['result']['fulfillment']['speech']
        if response:
            return response
        else:
            return 'error'
    except:
        return 'error'
