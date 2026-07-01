import requests
from bs4 import BeautifulSoup


def clean_title(title, source):
    suffix = f" - {source}"

    if title.endswith(suffix):
        return title[:-len(suffix)].strip()

    return title


def get_news(search_query, locale):
    user_agent = {
        'User-Agent': 'Mozilla/5.0'
    }

    url = "https://news.google.com/rss/search"

    params = {
        "q": f"{search_query} when:1d",
        "hl": locale["hl"],
        "gl": locale["gl"],
        "ceid": locale["ceid"]
    }

    response = requests.get(url, headers=user_agent, params=params, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "xml")

    items = soup.find_all("item")
    mass = []

    for item in items:
        title = item.find("title").get_text(strip=True)
        source = item.find("source").get_text(strip=True)

        news_item = {
            "title": clean_title(title, source),
            "link": item.find("link").get_text(strip=True),
            "date": item.find("pubDate").get_text(strip=True),
            "source": source
        }

        mass.append(news_item)

    return mass

