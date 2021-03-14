from flask import Flask
import requests
from bs4 import BeautifulSoup
import os
import sqlite3


URL = os.environ['SOURCE_URL']
AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

app = Flask(__name__)


def send_simple_message(title, message):
    return requests.post(
        os.environ['MAIL_URL'],
        auth=("api", os.environ['MAILGUN_API_KEY']),
        data={"from": "Embevent App <mailgun@sandboxfb0448ff1cfb4ffba160daeecce04274.mailgun.org>",
              "to": os.environ['MAIL_LIST'].split(";"),
              "subject": title,
              "text": message})

def processUpdates(cards):
    connection = sqlite3.connect("database.db")
    cursor = connection.execute("Select * from CARDS")
    old_cards = len(cursor.fetchall())

    if len(cards) > old_cards:
        
        card = cards[0]
        title    = card.find_all('h2', class_='h3')[0].text
        date     = card.find_all('h3', class_='h5')[0].text
        content  = card.find_all(["p", "div"])[0]

        command2 = "INSERT INTO CARDS  (title, date, content) VALUES ('{0}', '{1}', '{2}')".format(title,date,content)
        
        connection.execute(command2)
        connection.commit()
        connection.close()

        send_simple_message(title=title, message=card)
        return card.text
    else:
        f = cards[0]
        the_date, = f.find_all('h3', class_='h5')
        return "No news. Last update: {0}. articles available: {1}".format(the_date.text, old_cards)

@app.route('/')
def news():
    if not URL:
        return "No URL added"
    response = requests.get(URL, headers={'User-Agent': AGENT })
    soup = BeautifulSoup(response.content, 'html.parser')
    cards = soup.find_all('div', class_='card')
    return processUpdates(cards)