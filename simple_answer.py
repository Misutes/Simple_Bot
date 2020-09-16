import json

with open('key_words.json', 'r') as f:
    key_words = json.load(f)


def search_answer(_dict_, key_word, len_request):
    try:
        key_words["unresolved"] = 0
        function = _dict_[key_words[key_word]]
        return function
    except:
        key_words["unresolved"] += 1
        return _dict_["pass"]
    finally:
        if key_words["unresolved"] == len_request:
            key_words["unresolved"] = 0
            return _dict_["none"]
