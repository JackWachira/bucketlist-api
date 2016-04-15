"""Import statements."""
import nose
from flask_testing import TestCase
from app.bucketlist.models import db, User
from app import create_app
from config.config import TestingConfig



app = create_app(TestingConfig)

class BaseTestCase(TestCase):
    """Base configurations for the tests."""

    def create_app(self):
        """Set config options for the test app."""
        # app.config.from_object(TestingConfig)

        return app

    def setUp(self):
        """Set up the test client."""
        self.app = app.test_client()
        db.create_all()
        user = User("testuser")
        user.hash_password("testpassword")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """Destroy test db at end of tests."""
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    nose.run()
