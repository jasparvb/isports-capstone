"""Follow model tests."""

# run these tests like:
#
#    python -m unittest test_follow_model.py


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


class FollowModelTestCase(TestCase):
    """Test model for follows."""

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

    def test_follow_model(self):
        """Does basic model work?"""

        follow = Follow(
            name="Lionel Messi",
            user_id=self.u1.id,
            sportsdb_id="34146370",
            category="player",
            tb_image="https://www.thesportsdb.com/images/media/player/thumb/rgevg81516994688.jpg"
        )

        db.session.add(follow)
        db.session.commit()

        # User should have one follow
        self.assertEqual(len(self.u1.follows), 1)


    def test_valid_follow(self):
        """Does creating a follow work?"""
        follow = Follow(
            name="Lionel Messi",
            sportsdb_id="34146370",
            category="player",
            tb_image="https://www.thesportsdb.com/images/media/player/thumb/rgevg81516994688.jpg"
        )
        self.u1.follows.append(follow)
        db.session.commit()
        test_id = follow.id

        test_follow = Follow.query.get(test_id)

        self.assertEqual(test_follow.name, "Lionel Messi")
        self.assertEqual(test_follow.user_id, self.u1.id)


    def test_invalid_name(self):
        follow = Follow(
            name=None,
            sportsdb_id="34146370",
            category="player",
            tb_image="https://www.thesportsdb.com/images/media/player/thumb/rgevg81516994688.jpg"
        )
        self.u1.follows.append(follow)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()