from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Comment, Article
import datetime


class TestModels(TestCase):
    """Tests the models from blog app"""

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username="testuser",
                                             email="testuser@mail.com",
                                             password="testuserpssword1")

        cls.article = Article.objects.create(a_title="Article test",
                                             a_slug="article-test",
                                             a_content="lorem ipseum")
        cls.article_all = Article.objects.all()

        cls.comment = Comment.objects.create(on_article=cls.article_all.first(),
                                             by_user=User.objects.all().first(),
                                             comment_content="lorem ipseum 2")
        cls.comment_all = Comment.objects.all()

    def test_user_was_created(self):
        """Test the creation of a new user"""

        self.assertEqual(User.objects.all().count(), 1)

    def test_article_was_created(self):
        """Test the creation of an Article instance"""

        self.assertEqual(self.article_all.count(), 1)
        self.assertIsInstance(self.article_all.first().a_title, str)
        self.assertEqual(self.article_all.first().a_title, "Article test")
        self.assertIsInstance(self.article_all.first().a_slug, str)
        self.assertEqual(self.article_all.first().a_slug, "article-test")
        self.assertIsInstance(self.article_all.first().a_content, str)
        self.assertEqual(self.article_all.first().a_content, "lorem ipseum")
        self.assertIsInstance(self.article_all.first().a_pub_date, datetime.datetime)

    def test_comment_was_created(self):
        """Test the creation of a Comment instance"""

        self.assertEqual(self.comment_all.count(), 1)
        self.assertIsInstance(self.comment_all.first().on_article.a_title, str)
        self.assertEqual(self.comment_all.first().on_article.a_title, "Article test")
        self.assertIsInstance(self.comment_all.first().by_user.username, str)
        self.assertEqual(self.comment_all.first().by_user.username, "testuser")
        self.assertIsInstance(self.comment_all.first().comment_content, str)
        self.assertEqual(self.comment_all.first().comment_content, "lorem ipseum 2")
        self.assertIsInstance(self.comment_all.first().created_on, datetime.datetime)
