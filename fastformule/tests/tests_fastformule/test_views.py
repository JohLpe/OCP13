from django.test import TestCase, Client
from django.urls import reverse


class BlogViewTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.c = Client()

    def test_page_redirect(self):
        """Tests that homepage is accessible"""

        response = self.c.get(reverse('homepage'))
        self.assertRedirects(response,
                             expected_url="/saisons/actuelle/",
                             status_code=302,
                             target_status_code=200)
