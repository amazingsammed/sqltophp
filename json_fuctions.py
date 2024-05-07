import json


def loadJson(filename):
    try:
        file_contents = open(filename, "r").read()
        data = json.loads(file_contents)
        return data
    except Exception as e:
        print(e)
