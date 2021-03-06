import json
import re

import requests


def get_title(url):
    URL = f"https://api.upcitemdb.com/prod/trial/lookup?upc={url}"
    r = requests.get(URL)
    obj = json.loads(r.content)  # obj now contains a dict of the data
    try:
        print(obj)
        text = obj["items"][0]["title"]
    except (IndexError, KeyError) as e:
        URL = f"https://product-open-data.com/gtin/{url}"
        r = requests.get(URL)
        if r.status_code == 404:
            return "404"
        text = re.findall(r"<b>Commercial name<\/b> ?: ?(.+?) ?<br>", str(r.content))[0]
# Extracts the name of the product from the webpage
    return text

# based on the information in data.json, it routes to a different page
def get_type(title):
    title = title.lower()
    with open("data.json", "r") as f:
        data = json.loads(f.read())
    if title == "404":
        return "404"
    for item in data["ewaste"]:
        if item in title:
            return ["ewaste"]
    for item in data["compostable"]:
        if item in title:
            return ["compostable"]
    for item in data["recycle"]:
        if item in title:
            return ["recycle"]
    for item in data["trash"]:
        if item in title:
            return ["trash", item]
    return ["not in our database"]
