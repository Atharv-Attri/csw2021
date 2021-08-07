import requests
import json

def get_title(url):
    URL = f"https://api.upcitemdb.com/prod/trial/lookup?upc={url}"
    r = requests.get(URL)
    obj = json.loads(r.content)    # obj now contains a dict of the data
    text = obj['items'][0]['title']
    return text

print(get_title('0078742351889'))
