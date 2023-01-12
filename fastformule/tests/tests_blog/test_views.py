from django.test import TestCase, Client
from blog.models import Article, Comment
from django.urls import reverse
from django.contrib.auth.models import User


class BlogViewTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.c = Client()
        User.objects.create_user(username='usertest',
                                 password='testpwd')
        cls.user = User.objects.get(username='usertest')
        User.objects.create_user(username='staffuser',
                                 password='thisisastaffuserpsswrd',
                                 is_staff=True)
        cls.staff = User.objects.get(username='staffuser')
        cls.art = Article.objects.create(a_title="Mon titre test",
                                         a_slug="mon-titre-test",
                                         a_content="Lorem ipsum dolor sit amet")
        cls.art_all = Article.objects.all()
        cls.comm = Comment.objects.create(on_article=cls.art_all.first(),
                                          by_user=cls.user,
                                          comment_content="Excepteur sint occaecat")
        cls.comm_all = Comment.objects.all()

    def test_blog_page(self):
        """Tests that the blog page is accessible"""

        response = self.c.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)

    def test_view_article(self):
        """Tests that an article is accessible"""

        response = self.c.get(reverse('viewArticle',
                              args=[self.art_all.first().a_slug]))
        self.assertEqual(response.status_code, 200)

    def test_add_article_page_access_by_non_staff_user(self):
        """Tests that a non-staff user cannot access"""
        """page to add an article on blog"""

        self.assertEqual(self.art_all.count(), 1)
        self.assertFalse(self.user.is_staff)
        self.c.login(username='usertest', password='testpwd')
        self.assertTrue(self.user.is_authenticated)
        self.assertFalse(self.user.is_anonymous)

        response = self.c.get(reverse('addArticle'), follow=True)
        self.assertRedirects(response,
                             expected_url="/blog/",
                             status_code=302,
                             target_status_code=200)

    def test_add_article_page_access_by_staff_user(self):
        """Tests that a staff member can view"""
        """the page to add an article on blog"""

        self.assertEqual(self.art_all.count(), 1)
        self.assertTrue(self.staff.is_staff)
        self.c.login(username='staffuser',
                     password='thisisastaffuserpsswrd')
        self.assertTrue(self.staff.is_authenticated)
        self.assertFalse(self.staff.is_anonymous)

        response = self.c.get(reverse('addArticle'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_article_by_non_staff_user(self):
        """Tests that a non staff user cannot delete an article"""

        self.assertEqual(self.art_all.count(), 1)
        self.assertFalse(self.user.is_staff)
        self.c.login(username='usertest', password='testpwd')
        self.assertTrue(self.user.is_authenticated)
        self.assertFalse(self.user.is_anonymous)

        response = self.c.get(reverse('delArticle',
                              args=[self.art_all.first().id]),
                              follow=True)
        self.assertRedirects(response,
                             expected_url="/blog/",
                             status_code=302,
                             target_status_code=200)
        self.assertEqual(self.art_all.count(), 1)

    def test_delete_article_by_staff_user(self):
        """Tests that a staff member can delete an article on blog"""

        self.assertEqual(self.art_all.count(), 1)
        self.assertTrue(self.staff.is_staff)
        self.c.login(username='staffuser',
                     password='thisisastaffuserpsswrd')
        self.assertTrue(self.staff.is_authenticated)
        self.assertFalse(self.staff.is_anonymous)

        response = self.c.get(reverse('delArticle',
                                      args=[self.art_all.first().id]),
                              follow=True)
        self.assertRedirects(response,
                             expected_url="/blog/",
                             status_code=302,
                             target_status_code=200)
        self.assertEqual(self.art_all.count(), 0)

    def test_adding_an_article(self):
        """"Tests creation of an article on add_article page"""

        self.assertEqual(self.art_all.count(), 1)
        self.assertTrue(self.staff.is_staff)
        self.c.login(username='staffuser',
                     password='thisisastaffuserpsswrd')
        self.assertTrue(self.staff.is_authenticated)
        self.assertFalse(self.staff.is_anonymous)

        response = self.c.post(reverse('addArticle'),
                               {'a_title': "Titre 2 test",
                                'a_content': "Vivamus vulputate leo sed tempus."})
        self.assertEqual(self.art_all.count(), 2)
        self.assertEqual(self.art_all.last().a_title, "Titre 2 test")
        self.assertEqual(self.art_all.last().a_content,
                         "Vivamus vulputate leo sed tempus.")
        self.assertEqual(self.art_all.last().a_slug, "titre-2-test")
        self.assertRedirects(response,
                             expected_url="/blog/",
                             status_code=302,
                             target_status_code=200)

    def test_comment_on_article(self):
        """Tests the creation of a comment on an article"""

        self.assertFalse(self.user.is_staff)
        self.c.login(username='usertest', password='testpwd')
        self.assertTrue(self.user.is_authenticated)
        self.assertFalse(self.user.is_anonymous)

        self.assertEqual(self.comm_all.count(), 1)
        response = self.c.post(reverse('viewArticle', args=[self.art_all.first().a_slug]),
                               {'comment_content': "Mauris vestibulum mauris ut odio."})
        self.assertEqual(self.comm_all.count(), 2)
        self.assertEqual(self.comm_all.last().comment_content,
                         "Mauris vestibulum mauris ut odio.")
        self.assertEqual(self.comm_all.last().on_article.id,
                         self.art_all.first().id)
        self.assertEqual(self.comm_all.last().by_user.id, self.user.id)
        self.assertRedirects(response,
                             expected_url="/blog/{}/".format(self.art_all.first().a_slug),
                             status_code=302,
                             target_status_code=200)
