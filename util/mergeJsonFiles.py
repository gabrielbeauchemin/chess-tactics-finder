import json


def merge_json_file(file_path1, file_path2):
    with open(file_path1) as json_file1:
        with open(file_path2) as json_file2:
            json1 = json.load(json_file1)
            json2 = json.load(json_file2)
            return json1 + json2
