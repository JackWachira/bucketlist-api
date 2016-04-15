import json
from nose.tools import *
from app.bucketlist.resources import api, BucketList, Login
from tests import BaseTestCase


class TestAuthorizedBucketListOperations(BaseTestCase):

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
        """Test that a user can create a new bucketlist."""
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

    def test_list_bucketlists(self):
        """Test that a user can list all bucketlists."""
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        # create a test Bucketlist
        self.client.post(
            api.url_for(BucketList),
            data=json.dumps({"name": "testbucket"}),
            content_type='application/json',
            headers={'token': token}
        )

        # list all bucketlists
        bucketlists = self.client.get(api.url_for(BucketList, page=1, limit=2),
                                      content_type='application/json',
                                      headers={'token': token})

        self.assertEqual(bucketlists.status_code, 200)
        self.assertTrue(bucketlists)
        self.assertIn("testbucket", bucketlists.data)

    def test_list_search_bucketlists(self):
        """Test that a user can search and list bucketlists"""
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        # create a test Bucketlist
        self.client.post(
            api.url_for(BucketList),
            data=json.dumps({"name": "testbucket"}),
            content_type='application/json',
            headers={'token': token}
        )

        # list bucketlists with search
        bucketlists = self.client.get(api.url_for(
            BucketList, q='testbucket', page=1, limit=2), content_type='application/json', headers={'token': token})

        self.assertEqual(bucketlists.status_code, 200)
        self.assertTrue(bucketlists)
        self.assertIn("testbucket", bucketlists.data)

    def test_get_single_bucketlist(self):
        """Test that a user can get a single bucketlist."""
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        # create a test Bucketlist
        self.client.post(
            api.url_for(BucketList),
            data=json.dumps({"name": "testbucket"}),
            content_type='application/json',
            headers={'token': token}
        )

        # get a single bucket list
        bucketlists = self.client.get(api.url_for(BucketList, bucket_id=1),
                                      content_type='application/json',
                                      headers={'token': token})

        self.assertEqual(bucketlists.status_code, 200)
        self.assertIn("testbucket", bucketlists.data)

    def test_update_bucketlists(self):
        """Test that a user can update a certain bucketlist."""
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        # create a test Bucketlist
        self.client.post(
            api.url_for(BucketList),
            data=json.dumps({"name": "testbucket"}),
            content_type='application/json',
            headers={'token': token}
        )

        # assert testbucket is created
        bucketlists = self.client.get(api.url_for(BucketList),
                                      content_type='application/json',
                                      headers={'token': token})

        self.assertEqual(bucketlists.status_code, 200)
        self.assertIn("testbucket", bucketlists.data)

        # update the bucketlist
        updated_bucketlist = self.client.put(
            api.url_for(BucketList, bucket_id=1),
            data=json.dumps({"name": "testbucketupdated"}),
            content_type='application/json',
            headers={'token': token}
        )

        # assert bucketlist is updated
        self.assertEqual(updated_bucketlist.status_code, 200)
        self.assertIn("testbucketupdated", updated_bucketlist.data)

    def test_delete_bucketlists(self):
        """Test that a user can update a certain bucketlist."""
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        # create a test Bucketlist
        self.client.post(
            api.url_for(BucketList),
            data=json.dumps({"name": "testbucket"}),
            content_type='application/json',
            headers={'token': token}
        )

        # assert testbucket is created
        bucketlists = self.client.get(api.url_for(BucketList),
                                      content_type='application/json',
                                      headers={'token': token})

        self.assertEqual(bucketlists.status_code, 200)
        self.assertIn("testbucket", bucketlists.data)

        # delete the bucketlist
        response = self.client.delete(
            api.url_for(BucketList, bucket_id=1),
            content_type='application/json',
            headers={'token': token}
        )

        # assert bucketlist is deleted
        self.assertIn("Bucketlist 1 deleted successfully.", response.data)


class TestUnauthorizedBucketListOperations(BaseTestCase):
    def incorrent_login(self):
        username = "testwronguser"
        password = "testwrongpassword"

        response = self.client.post(
            api.url_for(Login),
            data=json.dumps(
                {'username': username,
                 'password': password
                 }),
            content_type='application/json'
        )
        return response

    def test_list_bucketlists_unathorized(self):
        """Test that an anauthorized user cannot search and list bucketlists"""
        token = 'wrongtoken'

        # create a test Bucketlist
        self.client.post(
            api.url_for(BucketList),
            data=json.dumps({"name": "testbucket"}),
            content_type='application/json',
            headers={'token': token}
        )

        # list bucketlists with search
        bucketlists = self.client.get(api.url_for(
            BucketList, q='testbucket', page=1, limit=2), content_type='application/json', headers={'token': token})

        self.assertEqual(bucketlists.status_code, 401)


class TestErrorsBucketListOperations(BaseTestCase):
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

    def test_create_bucketlist_with_wrong_params(self):
        """Test that a user cannot create a new bucketlist with missing params."""
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        # create a test Bucketlist
        response = self.client.post(
            api.url_for(BucketList),
            # wrong param 'something'
            data=json.dumps({"something": "testbucket"}),
            content_type='application/json',
            headers={'token': token}
        )

        # test bucketlist was not created
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Field may not be null.", data['error']['name'][0])

    # def test_create_bucketlist_with_wong_data_type(self):
    #     """Test that a user cannot create a new bucketlist with missing params."""
    #     response = self.login()
    #     message = json.loads(response.data)
    #     token = message['token']

    # create a test Bucketlist
    #     response = self.client.post(
    #         api.url_for(BucketList),
    #         data=json.dumps({"name": True}),
    #         content_type='application/json',
    #         headers={'token': token}
    #     )

    # test bucketlist was not created
    #     self.assertEqual(response.status_code, 400)
    #     data = json.loads(response.data)
    #     print data
    #     self.assertIn("Field may not be null.", data['name'])
