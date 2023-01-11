from django.test import TestCase
from django.test import Client
from user.forms import CreateUserForm


class BlogFormTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.c = Client()

    def test_user_form_is_valid(self):
        """Tests a valid UserForm"""

        form = CreateUserForm(data={'username':"Testertester",
                                    'email': "mytester@mail.com",
                                    'password1': "averyvalidpsswrd",
                                    'password2': "averyvalidpsswrd"})
        self.assertTrue(form.is_valid())

    def test_user_form_not_valid(self):
        """Tests a non-valid UserForm"""

        form = CreateUserForm(data={'username':"Testertester",
                                    'email': "mytester@mail.com",
                                    'password1': "averyvalidpsswrd",
                                    'password2': "notsovalidpsswrd"})
        self.assertFalse(form.is_valid())
