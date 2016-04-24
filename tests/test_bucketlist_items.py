import json
from nose.tools import *
from app.resources.resources import api, BucketListItem, BucketList, Login
from tests import BaseTestCase


class TestAuthorizedBucketListItemsOperations(BaseTestCase):

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

    def test_create_bucketlist_item(self):
        """Test that a user can create a new bucketlist item."""
        response = self.login()
        message = json.loads(response.data)
        token = message['Authorization']

        # create a test Bucketlist
        self.client.post(
            api.url_for(BucketList),
            data=json.dumps({"name": "testbucket"}),
            content_type='application/json',
            headers={'Authorization': token}
        )

        # create a test Bucketlist item
        response = self.client.post(
            api.url_for(BucketListItem, bucket_id=1),
            data=json.dumps({"name": "testbucketitem", "done": "false"}),
            content_type='application/json',
            headers={'Authorization': token}
        )

        # test bucketlist item was created
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("testbucketitem", data['name'])

    def test_update_bucketlist_item(self):
        """Test that a user can update a certain bucketlist item."""
        response = self.login()
        message = json.loads(response.data)
        token = message['Authorization']

        # create a test Bucketlist
        self.client.post(
            api.url_for(BucketList),
            data=json.dumps({"name": "testbucket"}),
            content_type='application/json',
            headers={'Authorization': token}
        )

        # create a test Bucketlist item
        response = self.client.post(
            api.url_for(BucketListItem, bucket_id=1),
            data=json.dumps({"name": "testbucketitem", "done": "false"}),
            content_type='application/json',
            headers={'Authorization': token}
        )

        # test bucketlist item was created
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("testbucketitem", data['name'])

        # update bucketlist item
        updated_bucketlist_item = self.client.put(
            api.url_for(BucketListItem, bucket_id=1, item_id=1),
            data=json.dumps(
                {"name": "testbucketitemupdated", "done": "false"}),
            content_type='application/json',
            headers={'Authorization': token}
        )

        # assert bucketlist item is updated
        self.assertEqual(updated_bucketlist_item.status_code, 200)
        self.assertIn("testbucketitemupdated", updated_bucketlist_item.data)

    def test_delete_bucketlists(self):
        """Test that a user can delete a certain bucketlist item."""
        response = self.login()
        message = json.loads(response.data)
        token = message['Authorization']

        # create a test Bucketlist
        self.client.post(
            api.url_for(BucketList),
            data=json.dumps({"name": "testbucket"}),
            content_type='application/json',
            headers={'Authorization': token}
        )

        # assert testbucket is created
        bucketlists = self.client.get(api.url_for(BucketList),
                                      content_type='application/json',
                                      headers={'Authorization': token})

        self.assertEqual(bucketlists.status_code, 200)
        self.assertIn("testbucket", bucketlists.data)

        # create a test Bucketlist item
        response = self.client.post(
            api.url_for(BucketListItem, bucket_id=1),
            data=json.dumps({"name": "testbucketitem", "done": "false"}),
            content_type='application/json',
            headers={'Authorization': token}
        )

        # test bucketlist item was created
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("testbucketitem", data['name'])

        # delete the bucketlist item
        response = self.client.delete(
            api.url_for(BucketListItem, bucket_id=1, item_id=1),
            content_type='application/json',
            headers={'Authorization': token}
        )

        # assert bucketlist item is deleted
        self.assertIn(
            "Bucketlist item 1 deleted successfully.", response.data)
