"""iSports: finds latest sports news headlines using newsapi.org"""

from random import randrange as random_num
from secret import API_KEY
import requests

def get_top_news():
    """Make API requests to return top sports news"""

    resp = requests.get(f"https://newsapi.org/v2/top-headlines?category=sports&country=us&apiKey={API_KEY}")

    return resp.json()["articles"][:7]


def get_all_news(term):
    """Make API request to return news matching search term"""

    resp = requests.get(f"https://newsapi.org/v2/everything", {"q":f"sports {term}", "language": "de", "apiKey": API_KEY})

    return resp.json()["articles"]


def get_my_news(term):
    """Make API request to return news matching followed item"""

    resp = requests.get(f"https://newsapi.org/v2/everything", {"q": term, "language": "en", "apiKey": API_KEY})

    return resp.json()["articles"]


def get_my_events(id, category):
    """Make API request to return events matching followed leagues and teams"""

    if category == "league":
        resp = requests.get(f"https://www.thesportsdb.com/api/v1/json/1/eventsnextleague.php?id={id}")
    else:
        resp = requests.get(f"https://www.thesportsdb.com/api/v1/json/1/eventsnext.php?id={id}")
    
    return resp.json()["events"]


def get_my_past_events(id, category):
    """Make API request to return past events matching followed leagues and teams"""

    if category == "league":
        resp = requests.get(f"https://www.thesportsdb.com/api/v1/json/1/eventspastleague.php?id={id}")
    else:
        resp = requests.get(f"https://www.thesportsdb.com/api/v1/json/1/eventslast.php?id={id}")
    
    return resp.json()["events"]
