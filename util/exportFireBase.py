import json
from Requests import requests


def export_to_firebase(tactics):
    with open('data.txt') as json_file:
        problems = json.load(json_file)
        r = requests.put("https://chess-db-3b296.firebaseio.com/whoWin.json",
                         data=problems.pop())
        for problem in tactics:
            r = requests.post("https://chess-db-3b296.firebaseio.com/whoWin.json",
                              data=problem)
