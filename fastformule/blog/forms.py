from django.forms import ModelForm
from .models import Article, Comment


class ArticleForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Article
        fields = ['a_title', 'a_content']


class CommentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = ['comment_content']
