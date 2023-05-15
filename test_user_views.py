"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User
from forms import UserAddForm

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Tests for user routes."""

    def setUp(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['curr_user'] = None
            
            User.query.delete()
            Message.query.delete()

            self.testuser = User.signup(username="testuser",
                                email="test@test.com",
                                password="testuser",
                                image_url=None)
            
            db.session.commit()

    def test_add_user(self):
        """tests the adding user functionality"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                username='testuser2'
                email='test2@test.com'
                password='testuser2'
                image_url=None

                res = client.post('/signup', data= { username:'testuser2', 
                                                   email:'test2@test.com', 
                                                   password:'testuser2',
                                                   image_url:None }, follow_redirects=True)

                self.assertEqual(res.status_code, 200)
                print(User.query.all())
                self.assertIsNotNone(User.query.filter_by(username='testuser2').first())

