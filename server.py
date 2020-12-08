from flask import Flask
import requests
from bs4 import BeautifulSoup
import os


URL = os.environ['SOURCE_URL']
AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
MIN = 11

app = Flask(__name__)

def processUpdates(cards):
    if len(cards) > MIN:
        return "New announcement happened!. Mail will be sent in a next release"
    else:
        f = cards[0]
        the_date, = f.find_all('h3', class_='h5')
        return "No news. Last update: {0}".format(the_date.text)

@app.route('/')
def news():
    if not URL:
        return "No URL added"
    response = requests.get(URL, headers={'User-Agent': AGENT })
    soup = BeautifulSoup(response.content, 'html.parser')
    cards = soup.find_all('div', class_='card')
    return processUpdates(cards)