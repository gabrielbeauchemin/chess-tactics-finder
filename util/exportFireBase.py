import json
import random

import requests


def export_to_firebase(tactics_file):
    with open(tactics_file) as json_file:
        problems = json.load(json_file)
        for problem in problems:
            problem["random"] = random.uniform(0, 1)
            r = requests.post("",
                      data=json.dumps(problem))
