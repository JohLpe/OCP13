from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    """Blog article"""

    a_title = models.CharField(max_length=150)
    a_slug = models.SlugField(unique=True, allow_unicode=True)
    a_content = models.TextField()
    a_pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Class Article, named {}".format(self.a_title)


class Comment(models.Model):
    """Comments under articles"""

    on_article = models.ForeignKey(Article,
                                   on_delete=models.CASCADE,
                                   related_name='comments')
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment on {} by {}'.format(self.on_article, self.by_user)
