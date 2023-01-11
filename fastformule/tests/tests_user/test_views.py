from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class BlogViewTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.c = Client()
        User.objects.create_user("TestUser",
                                 "usertest@mail.com",
                                 "psswordforauser")
        cls.user_test = User.objects.get(username="TestUser")

    def test_registration_page(self):
        """Tests access to registration page"""

        response = self.c.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        """Tests access to the login page"""

        response = self.c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_redirect(self):
        """Tests redirection after log out"""

        response = self.c.get(reverse('logout'), follow=True)
        self.assertRedirects(response,
                             expected_url="/saisons/current/",
                             status_code=302,
                             target_status_code=200)

    def test_account_page(self):
        """Tests access to account page for logged in user"""

        self.c.login(username="TestUser",
                     password="psswordforauser")
        self.assertTrue(self.user_test.is_authenticated)
        self.assertFalse(self.user_test.is_anonymous)
        response = self.c.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
