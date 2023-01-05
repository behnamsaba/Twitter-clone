"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from app import app

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
app.config['SQLALCHEMY_ECHO'] = False



# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
        

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            id=1,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(u.__repr__(),'<User #1: testuser, test@test.com>') #repr test

    def test_following(self):
        user1=User(
            email="user1",
            username="testuser1",
            password="1234"
        )

        user2=User(
            email="user2",
            username="testuser2",
            password="1234"
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.assertFalse(user1.is_followed_by(user2))
    
    def test_followers(self):
        user1=User(
            email="user1",
            username="testuser1",
            password="1234"
        )

        user2=User(
            email="user2",
            username="testuser2",
            password="1234"
        )

        user1.following.append(user2)
        user2.followers.append(user1)
        self.assertTrue(user1.is_following(user2))
        self.assertTrue(user2.is_followed_by(user1))

    def test_signup(self):
        user=User.signup(username="testuser1", email="user1", password="1234", image_url="/static/images/default-pic.png")
        self.assertTrue(user)

    def test_signup_nullable(self):
        with self.assertRaises(Exception):
            User.signup(username="testuser1", email="user1") #return error not valid
    
    def test_authenticate(self):
        user1=User.signup(username="testuser1", email="user1", password="1234",image_url="/static/images/default-pic.png")
        db.session.add(user1)
        db.session.commit()
        self.assertTrue(User.authenticate(username="testuser1",password="1234"))
    
    def test_authenticate_not_valid(self):
        user1=User.signup(username="testuser1", email="user1", password="1234",image_url="/static/images/default-pic.png")
        db.session.add(user1)
        db.session.commit()
        self.assertTrue(User.authenticate(username="testuser1",password="1234")) #true user pass
        self.assertFalse(User.authenticate(username="empty",password="1234")) #user not valid
        self.assertFalse(User.authenticate(username="testuser1",password="not valid")) #pass not valid



