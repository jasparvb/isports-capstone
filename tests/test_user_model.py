"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


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


class UserModelTestCase(TestCase):
    """Test model for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Favorite.query.delete()
        Follow.query.delete()

        u1 = User.signup(
            username="messi10",
            email="messi@fcb.es",
            password="G.O.A.T",
        )

        db.session.commit()

        fav1 = Favorite(
            title="Bundesliga droht TV-Blackout am ersten Spieltag des Re-Starts - Digitalfernsehen.de",
            url="https://www.digitalfernsehen.de/news/medien-news/maerkte/bundesliga-droht-tv-blackout-am-ersten-spieltag-des-re-starts-556301/",
            image_url="https://www.digitalfernsehen.de/wp-content/uploads/2019/11/Testbild.jpg",
            published_at="2020-05-15T17:17:28Z",
            user_id=u1.id
        )

        follow1 = Follow(
            name="Lionel Messi",
            user_id=u1.id,
            sportsdb_id="34146370",
            category="player",
            tb_image="https://www.thesportsdb.com/images/media/player/thumb/rgevg81516994688.jpg"
        )

        
        self.u1 = u1
        self.fav1 = fav1
        self.follow1 = follow1
        self.client = app.test_client()


    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no follows & no favorites
        self.assertEqual(len(u.follows), 0)
        self.assertEqual(len(u.favorites), 0)


    def test_follows(self):
        self.u1.follows.append(self.follow1)
        db.session.commit()

        self.assertEqual(len(self.u1.follows), 1)


    def test_favorites(self):
        self.u1.favorites.append(self.fav1)
        db.session.commit()

        self.assertEqual(len(self.u1.favorites), 1)


    def test_valid_signup(self):
        """Does signup work?"""
        u = User.signup(username="terstegen1", email="terstegen@fcb.es", password="W.A.L.L")
        db.session.commit()
        test_id = u.id

        test_user = User.query.get(test_id)

        self.assertEqual(test_user.username, "terstegen1")
        self.assertEqual(test_user.email, "terstegen@fcb.es")
        self.assertNotEqual(test_user.password, "W.A.L.L")


    def test_invalid_username(self):
        u = User.signup(username=None, email="terstegen@fcb.es", password="W.A.L.L")
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()


    def test_username_not_unique(self):
        u = User.signup(username="messi10", email="terstegen@fcb.es", password="W.A.L.L")
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()


    def test_invalid_password(self):
        with self.assertRaises(ValueError) as context:
            u = User.signup(username="messi10", email="terstegen@fcb.es", password=None)


    def test_authentication_valid_input(self):
        """Does authentication work?"""
        self.assertEqual(User.login("messi10", "G.O.A.T"), self.u1)


    def test_authentication_invalid_username(self):
        self.assertFalse(User.login("messi11", "G.O.A.T."))


    def test_authentication_invalid_password(self):
        self.assertFalse(User.login("messi10", "G.O.A.T.2"))