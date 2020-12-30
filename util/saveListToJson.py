import json


def save_list_to_json(list_obj, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(list_obj, default=lambda obj: obj.__dict__))
