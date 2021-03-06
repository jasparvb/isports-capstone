"""iSports: finds latest sports news headlines using newsapi.org"""

from secret import API_KEY
import requests

class Isports():

    def __init__(self):

        self.languages = [
                {"value": "en", "label": "English"},
                {"value": "es", "label": "Spanish"},
                {"value": "de", "label": "German"},
                {"value": "fr", "label": "French"},
                {"value": "it", "label": "Italian"}]

    def get_top_news(self, lang="us"):
        """Make API requests to return top sports news. Convert lang code to country code where different"""
        if lang == "en":
            lang = "us"
        if lang == "es":
            lang = "mx"

        resp = requests.get(f"https://newsapi.org/v2/top-headlines", {"category": "sports", "pageSize": 7, "country": lang, "apiKey": API_KEY})

        return resp.json()["articles"]


    def get_all_news(self, term, lang="en", page=1):
        """Make API request to return news matching search term"""

        resp = requests.get(f"https://newsapi.org/v2/everything", {"q":f"sports {term}", "pageSize": 15, "page": page, "language": lang, "apiKey": API_KEY})

        return resp.json()["articles"]


    def get_my_news(self, term, lang="en", page=1):
        """Make API request to return news matching followed item"""

        resp = requests.get(f"https://newsapi.org/v2/everything", {"q": term, "pageSize": 7, "page": page, "language": lang, "apiKey": API_KEY})
        if resp.json()["status"] == "ok":
            return resp.json()["articles"]
        return {"error": "Max reached"}


    def get_my_events(self, id, category):
        """Make API request to return events matching followed leagues and teams"""

        if category == "league":
            resp = requests.get(f"https://www.thesportsdb.com/api/v1/json/1/eventsnextleague.php?id={id}")
        else:
            resp = requests.get(f"https://www.thesportsdb.com/api/v1/json/1/eventsnext.php?id={id}")
        
        return resp.json()["events"]


    def get_my_past_events(self, id, category):
        """Make API request to return past events matching followed leagues and teams"""

        if category == "league":
            resp = requests.get(f"https://www.thesportsdb.com/api/v1/json/1/eventspastleague.php?id={id}")
        else:
            resp = requests.get(f"https://www.thesportsdb.com/api/v1/json/1/eventslast.php?id={id}")
        
        return resp.json()

    def get_league_image(self, id):
        """Make API request to return league badge given an id"""

        resp = requests.get(f"https://www.thesportsdb.com/api/v1/json/1/lookupleague.php?id={id}")

        return resp.json()["leagues"][0]["strBadge"]