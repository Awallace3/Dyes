import requests
import json


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


url = 'http://127.0.0.1:8080/submit'
myobj = read_json('./test.json')

x = requests.post(url, data=myobj)

print(x.text)
