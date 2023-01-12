from . import views
from django.urls import path

urlpatterns = [
    path('blog/', views.view_blog, name='blog'),
    path('blog/add/', views.add_article, name='addArticle'),
    path('blog/<slug:slug>/', views.view_article, name='viewArticle'),
    path('delete-entry/<int:art_id>/',
         views.delete_article, name='delArticle'),
    path('delete-comment/<int:comm_id>/',
         views.delete_comment, name='delComment'),
    path('edit-comment/',
         views.edit_comment, name='editComment'),
]
