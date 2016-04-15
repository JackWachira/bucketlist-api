import json
from nose.tools import *
from app.bucketlist.resources import BucketList,Login
from tests import BaseTestCase

class TestBucketListOperations(BaseTestCase):

    def login(self):
        username = "testuser"
        password = "testpassword"

        response = self.client.post(
                                    api.url_for(Login),
                                    data=json.dumps(
                                            {'username': username,
                                             'password': password
                                             }),
                                    content_type='application/json'
                                    )
        return response

    def test_create_bucketlist(self):
        """Test that a user can create bucketlist."""
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        # create a test Bucketlist
        response = self.client.post(
                         api.url_for(BucketList),
                         data=json.dumps({"name": "testbucket"}),
                         content_type='application/json',
                         headers={'token': token}
                         )

        # test bucketlist was created
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("testbucket", data['name'])
