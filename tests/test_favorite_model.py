"""Favorite model tests."""

# run these tests like:
#
#    python -m unittest test_favorite_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Favorite, Follow

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql://postgres:41361@localhost/isports_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class FavoriteModelTestCase(TestCase):
    """Test model for favorites."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Follow.query.delete()
        Favorite.query.delete()

        u1 = User.signup(
            username="messi10",
            email="messi@fcb.es",
            password="G.O.A.T",
        )

        db.session.commit()

        self.u1 = u1
        self.client = app.test_client()


    def tearDown(self):
        db.session.rollback()

    def test_favorite_model(self):
        """Does basic model work?"""

        fav = Favorite(
            title="Bundesliga droht TV-Blackout am ersten Spieltag des Re-Starts - Digitalfernsehen.de",
            url="https://www.digitalfernsehen.de/news/medien-news/maerkte/bundesliga-droht-tv-blackout-am-ersten-spieltag-des-re-starts-556301/",
            image_url="https://www.digitalfernsehen.de/wp-content/uploads/2019/11/Testbild.jpg",
            published_at="2020-05-15T17:17:28Z",
            user_id=self.u1.id
        )

        db.session.add(fav)
        db.session.commit()

        # User should have one follow
        self.assertEqual(len(self.u1.favorites), 1)


    def test_valid_favorite(self):
        """Does creating a favorite work?"""
        fav = Favorite(
            title="Bundesliga droht TV-Blackout am ersten Spieltag des Re-Starts - Digitalfernsehen.de",
            url="https://www.digitalfernsehen.de/news/medien-news/maerkte/bundesliga-droht-tv-blackout-am-ersten-spieltag-des-re-starts-556301/",
            image_url="https://www.digitalfernsehen.de/wp-content/uploads/2019/11/Testbild.jpg",
            published_at="2020-05-15T17:17:28Z",
        )
        self.u1.favorites.append(fav)
        db.session.commit()
        test_id = fav.id

        test_fav = Favorite.query.get(test_id)

        self.assertEqual(test_fav.title, "Bundesliga droht TV-Blackout am ersten Spieltag des Re-Starts - Digitalfernsehen.de")
        self.assertTrue(test_fav.published_at)
        self.assertEqual(test_fav.user_id, self.u1.id)
      