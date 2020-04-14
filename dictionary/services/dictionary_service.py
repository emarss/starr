import json
from difflib import get_close_matches


def perfom_search(w):
    data = json.load(open("media/dictionary/data.json"))
    if w in data:
        return  {
            "result": "found",
            "response": data[w]
        }
    elif w.lower() in data:
        return  {
            "result": "found",
            "response": data[w.lower()]
        }
    elif len(get_close_matches(w, data.keys())) > 0:
        return  {
            "result": "close_matches",
            "response": get_close_matches(w, data.keys())[:]
        }
    else:
        return  {
            "result": "not_found",
            "response": "The word doesn't exist. Please double check it."
        }
