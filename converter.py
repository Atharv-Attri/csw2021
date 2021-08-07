import requests
import json

def get_title(url):
    URL = f"https://api.upcitemdb.com/prod/trial/lookup?upc={url}"
    r = requests.get(URL)
    obj = json.loads(r.content)    # obj now contains a dict of the data
    try:
        text = obj['items'][0]['title']
    except IndexError:
        return "404"
    return text


def get_type(title):
    title = title.lower()
    with open("data.json", "r") as f:
        data = json.loads(f.read())
    if title == "404":
        return "404"
    for item in data["ewaste"]:
        if item in title:
            return "ewaste"
    for item in data["compostable"]:
        if item in title:
            return "compostable"
    for item in data["recycle"]:
        if item in title:
            return "recycle"
    return "not in our database"

print(get_type(get_title('0078742351889')))