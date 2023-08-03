from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('',
         views.index,
         name='index'),
    path('posts/<int:id>/',
         views.post_detail,
         name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts,
         name='category_posts'),
    path('profile/<str:user_name>/',
         views.user_profile,
         name='profile'),
    path('edit/<str:user_name>/',
         views.edit_profile,
         name='edit_profile'),
    path('posts/create/',
         views.CreatePostView.as_view(),
         name='create_post'),
    path('posts/<int:pk>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<int:pk>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),
    path('post/<int:pk>/comment/',
         views.CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:pk>/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:pk>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'),
]
