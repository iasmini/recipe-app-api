from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


# helper function to create user
# **param - dynamic list of arguments
def create_user(**params):
    return get_user_model().objects.create_user(**params)


# the instructor separates in public and private
# the public api is unauthenticated
# the private api is authenticated
class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        # it simplifies to call our client in our test to not have to create it
        # manually in every single test we run
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        # the payload is the object that you pass to the api in the request
        payload = {
            'email': 'test@test.com',
            'password': '123',
            'name': 'test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # test if the object was actually created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # unwind the response - it'll take the dictionary response (similar to
        # the payload dictionary, plus id field)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        # test if the password is not in the res.data, for security it
        # shouldnt be
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@test.com', 'password': '1234'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test thar the password must be more than 1 character"""
        payload = {'email': 'test@test.com', 'password': '123'}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # if the user exists it will return true
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)