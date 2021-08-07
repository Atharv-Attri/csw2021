import requests
from bs4 import BeautifulSoup


def get_title(url):
    URL = f"https://www.barcodable.com/upc/{url}"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    text = soup.findAll('h2', {'class': 'mb64 mb-xs-32'})[0].text
    return text

print(get_title('041900076382'))
