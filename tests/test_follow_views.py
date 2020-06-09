"""Follow View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_follow_views.py


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


    def test_add_follow(self):
        """Can user add a follow?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/follow", data={"name": "Lionel Messi",
                                            "sportsdb_id": "34146370",
                                            "category": "player",
                                            "tb_image": "https://www.thesportsdb.com/images/media/player/thumb/rgevg81516994688.jpg"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            follow = Follow.query.one()
            self.assertEqual(follow.name, "Lionel Messi")
            self.assertEqual(follow.user_id, self.testuser.id)


    def test_add_follow_not_logged_in(self):
        """Can you add a follow when not logged in?"""

        with self.client as c:
            resp = c.post("/follow", data={"name": "Lionel Messi",
                                            "sportsdb_id": "34146370",
                                            "category": "player",
                                            "tb_image": "https://www.thesportsdb.com/images/media/player/thumb/rgevg81516994688.jpg"}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must log in to access that page.', html)


    def test_add_follow_invalid_input(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/follow", data={"name": "alskdjfowief"}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Invalid input! Select an item from the list.', html)


    def test_delete_follow(self):
        """Can user delete a follow?"""
        follow = Follow(name="Lionel Messi",
                        sportsdb_id="34146370",
                        category="player",
                        tb_image="https://www.thesportsdb.com/images/media/player/thumb/rgevg81516994688.jpg")
        self.testuser.follows.append(follow)
        db.session.commit()
        test_id = follow.id

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post(f"/follow/{test_id}/delete", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            follow = Follow.query.get(test_id)
            self.assertIsNone(follow)


    def test_delete_follow_not_logged_in(self):
        """Can you delete a follow when not logged in?"""
        follow = Follow(name="Lionel Messi",
                        sportsdb_id="34146370",
                        category="player",
                        tb_image="https://www.thesportsdb.com/images/media/player/thumb/rgevg81516994688.jpg")
        self.testuser.follows.append(follow)
        db.session.commit()
        test_id = follow.id

        with self.client as c:

            resp = c.post(f"/follow/{test_id}/delete", follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must log in to access that page.', html)

            follow = Follow.query.get(test_id)
            self.assertIsNotNone(follow)
