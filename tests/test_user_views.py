"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, User, Follow, Favorite

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql://postgres:41361@localhost/isports_test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Follow.query.delete()
        Favorite.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser")

        db.session.commit()

        self.follow = Follow(name="Lionel Messi",
                            sportsdb_id="34146370",
                            category="player",
                            tb_image="https://www.thesportsdb.com/images/media/player/thumb/rgevg81516994688.jpg")

        self.fav = Favorite(title="Bundesliga droht TV-Blackout am ersten Spieltag des Re-Starts - Digitalfernsehen.de",
                            url="https://www.digitalfernsehen.de/news/medien-news/maerkte/bundesliga-droht-tv-blackout-am-ersten-spieltag-des-re-starts-556301/",
                            image_url="https://www.digitalfernsehen.de/wp-content/uploads/2019/11/Testbild.jpg",
                            published_at="2020-05-15T17:17:28Z")


        self.testuser.follows.append(self.follow)
        self.testuser.favorites.append(self.fav)

        db.session.commit()

            
    def test_news_search(self):
        """Does the list of articles display with a search parameter?"""

        with self.client as c:
            resp = c.get("/search?q=messi")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Results for "messi"</h1>', html)

            
    def test_show_user_profile(self):
        """Does the user profile display correctly?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"/user")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>iSports profile for testuser</h1>', html)


    def test_show_user_news(self):
        """Does user news page display correctly?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"/news")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>News for testuser</h1>', html)


    def test_show_user_events(self):
        """Does the user events page display correctly?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"/events")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Sports events for testuser</h1>', html)


    def test_show_user_favorites(self):
        """Does the user favorites page display correctly?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"/favorites")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Saved articles</h1>', html)

    
    def test_show_user_profile_not_logged_in(self):
        """Can you view user profile when not logged in?"""

        with self.client as c:
            resp = c.get(f"/user", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must log in to access that page.', html)


    def test_show_user_news_not_logged_in(self):
        """Can you view user news when not logged in?"""

        with self.client as c:
            resp = c.get(f"/news", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must log in to access that page.', html)


    def test_show_user_events_not_logged_in(self):
        """Can you view user events when not logged in?"""

        with self.client as c:
            resp = c.get(f"/events", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must log in to access that page.', html)


    def test_show_user_favorites_not_logged_in(self):
        """Can you view user favorites when not logged in?"""

        with self.client as c:
            resp = c.get(f"/favorites", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must log in to access that page.', html)
