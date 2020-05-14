"""iSports: finds latest sports news headlines using newsapi.org"""

from random import randrange as random_num
from secret import API_KEY
import requests

def get_top_news():
    """Make API requests to return top sports news"""

    resp = requests.get(f"https://newsapi.org/v2/top-headlines?category=sports&country=us&apiKey={API_KEY}")

    return resp.json()["articles"][:7]