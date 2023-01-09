from django.test import TestCase, Client
from django.urls import reverse


class BlogViewTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.c = Client()

    def test_blog_page(self):
        """Tests that the blog page is accessible"""

        response = self.c.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
