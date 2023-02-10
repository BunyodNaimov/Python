from python_exceptions import write_exceptions
import json


def get_data():
    file = None
    try:
        with open("tashkent.json", encoding="utf8") as f:
            file = json.load(f)
    except FileNotFoundError as e:
        write_exceptions(e)
    return file

