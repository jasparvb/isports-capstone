"""Favorite View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_favorite_views.py


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

FAV_DATA = {"title": "Bundesliga droht TV-Blackout am ersten Spieltag des Re-Starts - Digitalfernsehen.de",
            "url": "https://www.digitalfernsehen.de/news/medien-news/maerkte/bundesliga-droht-tv-blackout-am-ersten-spieltag-des-re-starts-556301/",
            "image_url": "https://www.digitalfernsehen.de/wp-content/uploads/2019/11/Testbild.jpg",
            "published_at": "2020-05-15T17:17:28Z"}


class FollowViewTestCase(TestCase):
    """Test views for follows."""

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


    def test_add_favorite(self):
        """Can user add a favorite?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/favorites", json=FAV_DATA)

            self.assertEqual(resp.status_code, 201)

            favorite = Favorite.query.one()
            self.assertEqual(favorite.title, "Bundesliga droht TV-Blackout am ersten Spieltag des Re-Starts - Digitalfernsehen.de")
            self.assertEqual(favorite.user_id, self.testuser.id)
            self.assertEqual(resp.json, {"favorite":{"id": favorite.id}})


    def test_add_favorite_not_logged_in(self):
        """Can you add a favorite when not logged in?"""

        with self.client as c:
            resp = c.post("/favorites", json=FAV_DATA, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must log in to access that page.', html)


    def test_delete_favorite(self):
        """Can user delete a favorite?"""
        favorite = Favorite(title="Bundesliga droht TV-Blackout am ersten Spieltag des Re-Starts - Digitalfernsehen.de",
                            url="https://www.digitalfernsehen.de/news/medien-news/maerkte/bundesliga-droht-tv-blackout-am-ersten-spieltag-des-re-starts-556301/",
                            image_url="https://www.digitalfernsehen.de/wp-content/uploads/2019/11/Testbild.jpg",
                            published_at="2020-05-15T17:17:28Z")
        self.testuser.favorites.append(favorite)
        db.session.commit()
        test_id = favorite.id

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.delete(f"/favorites/{test_id}", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            favorite = Favorite.query.get(test_id)
            self.assertIsNone(favorite)


    def test_delete_favorite_not_logged_in(self):
        """Can you delete a favorite when not logged in?"""
        favorite = Favorite(title="Bundesliga droht TV-Blackout am ersten Spieltag des Re-Starts - Digitalfernsehen.de",
                            url="https://www.digitalfernsehen.de/news/medien-news/maerkte/bundesliga-droht-tv-blackout-am-ersten-spieltag-des-re-starts-556301/",
                            image_url="https://www.digitalfernsehen.de/wp-content/uploads/2019/11/Testbild.jpg",
                            published_at="2020-05-15T17:17:28Z")
        self.testuser.favorites.append(favorite)
        db.session.commit()
        test_id = favorite.id

        with self.client as c:

            resp = c.delete(f"/favorites/{test_id}", follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must log in to access that page.', html)

            favorite = Favorite.query.get(test_id)
            self.assertIsNotNone(favorite)
