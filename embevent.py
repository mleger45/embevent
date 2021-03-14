import requests
from bs4 import BeautifulSoup
from server import processUpdates, AGENT, URL


def news():
    if not URL:
        return "No URL added"
    response = requests.get(URL, headers={'User-Agent': AGENT })
    soup = BeautifulSoup(response.content, 'html.parser')
    cards = soup.find_all('div', class_='card')
    return processUpdates(cards)

if __name__ == "__main__":
    news()