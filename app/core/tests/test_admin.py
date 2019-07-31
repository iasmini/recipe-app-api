from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        # sets to self to be accessible in the other test a client variable
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='test@test.com',
            password='123'
        )
        # client helper function: allows you to log a user in the django
        # authentication so we dont have to manually log the user
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='123',
            name='test name'
        )