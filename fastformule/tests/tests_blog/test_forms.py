from django.test import TestCase
from django.test import Client
from blog.forms import ArticleForm, CommentForm


class BlogFormTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.c = Client()

    def test_ArticleForm_valid(self):
        """Tests a valid form for ArticleForm"""

        form = ArticleForm(data={'a_title': "Titre test",
                                 'a_content': "Lorem ipsum dolor sit amet"})
        self.assertTrue(form.is_valid())

    def test_ArticleForm_invalid(self):
        """Tests an invalid form for ArticleForm"""

        form = ArticleForm(data={'a_title': "", 'a_content': ""})
        self.assertFalse(form.is_valid())

    def test_CommentForm_valid(self):
        """Tests a valid form for CommentForm"""

        form = CommentForm(data={'comment_content': "Lorem ipsum dolor sit"})
        self.assertTrue(form.is_valid())

    def test_CommentForm_invalid(self):
        """Tests an invalid form for CommentForm"""

        form = CommentForm(data={'comment_content': ""})
        self.assertFalse(form.is_valid())
