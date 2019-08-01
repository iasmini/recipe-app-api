from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        # sets to self to be accessible in the other test a client variable
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='test1@test.com',
            password='123'
        )
        # client helper function: allows you to log a user in the django
        # authentication so we dont have to manually log the user
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test2@test.com',
            password='123',
            name='test name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # reverse - if we need to change the url in future we dont need to
        # worry because reverse will do it automatically
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # checks if the response contains a certain item
        # checks that http response was http 200
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
