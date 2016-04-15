import json
from nose.tools import *
from app.resources.resources import api, Login, Register
from tests import BaseTestCase


class TestAuthentication(BaseTestCase):

    def login_correct(self):
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

    def login_incorrect(self):
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

    def test_user_login_successful(self):
        """Test that a user can login successfully"""
        response = self.login_correct()
        message = json.loads(response.data)
        token = message['token']

        # check if token received
        self.assertTrue(token)
        # check response code
        self.assertEqual(response.status_code, 200)

    def test_user_login_fail(self):
        """Test that a user cannot login with incorrect credentials"""
        response = self.login_incorrect()
        # check response code
        self.assertEqual(
            json.loads(response.data)['error'], "Incorrect Login credentials")

    def test_user_register_successful(self):
        """Test that a user can register successfully"""

        # create a test user
        response = self.client.post(
            api.url_for(Register),
            data=json.dumps({"username": "tim", "password": "doe"}),
            content_type='application/json',
        )

        # log in with the user
        response = self.client.post(
            api.url_for(Login),
            data=json.dumps(
                {'username': "tim",
                 'password': "doe"
                 }),
            content_type='application/json'
        )

        message = json.loads(response.data)
        token = message['token']

        # check if token received
        self.assertTrue(token)
        # check response code
        self.assertEqual(response.status_code, 200)
