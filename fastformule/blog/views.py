from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.core.paginator import Paginator
from slugify import slugify
from django.http import JsonResponse
from django.core import serializers
import json


def view_blog(request):
    """Renders blog page"""

    article_list = Article.objects.all().order_by('a_pub_date')
    paginator = Paginator(article_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'page_obj': page_obj})


@user_passes_test(lambda user: user.is_staff,
                  login_url="blog", redirect_field_name=None)
def add_article(request):
    """Renders page to add a new article to blog"""

    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.a_slug = slugify(new_article.a_title)
            new_article.save()

            return redirect('blog')

    return render(request, 'add.html', context={'form': form})


def view_article(request, slug):
    """Renders page to add a new article to blog"""

    my_article = Article.objects.get(a_slug=slug)
    comment = Comment.objects.filter(on_article=my_article.id)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.by_user = request.user
            new_comment.on_article = my_article
            new_comment.save()

            return redirect('viewArticle', slug=slug)

    return render(request, 'article.html', context={'article': my_article,
                                                    'form': form,
                                                    'comments': comment})


@user_passes_test(lambda user: user.is_staff,
                  login_url="blog", redirect_field_name=None)
def delete_article(request, art_id):
    """Deletes an article on blog"""

    try:
        Article.objects.get(id=art_id).delete()
    except Exception:
        print('No article found')
        return redirect('blog')

    return redirect('blog')


def delete_comment(request, comm_id):
    """Deletes a comment on an article on blog"""

    try:
        on_article = Comment.objects.get(id=comm_id).on_article.id
        get_article = Article.objects.get(id=on_article).a_slug
        Comment.objects.get(id=comm_id).delete()

    except Exception:
        print('No comment found')
        return redirect('viewArticle', slug=get_article)

    return redirect('viewArticle', slug=get_article)


def edit_comment(request):
    """Edits a comment on an article on blog"""

    if request.method == 'POST':
        comment_to_edit = request.POST.get('comment')
        content_to_update = request.POST.get('content')
        Comment.objects.filter(id=comment_to_edit).update(comment_content=content_to_update)
        updated_comment = serializers.serialize("json",
                                                Comment.objects.filter(id=comment_to_edit))
        response = json.loads(updated_comment)

    return JsonResponse(response, safe=False)
