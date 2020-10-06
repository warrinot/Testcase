from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [

    path('', login_required(views.PostListView.as_view()), name='post_list'),
    path('post/<int:pk>', login_required(views.PostDetailView.as_view()), name='post_detail'),
    path('create/', login_required(views.PostCreateView.as_view()), name='post_create'),
    path('post/update/<int:pk>', login_required(views.PostUpdateView.as_view()),
         name='post_update'),
    path('post/delete/<int:pk>', login_required(views.PostDeleteView.as_view()),
         name='post_delete'),
    path('blogs/<user>/', login_required(views.UserPostPage.as_view()), name='user_page'),
    path('feed/', login_required(views.personal_feed), name='feed'),
    path('post/<int:post_id>/make_seen/', views.make_post_seen, name='make_seen'),
    path('posts/draft/', login_required(views.PostDraftView.as_view()), name='draft_posts'),
    path('posts/add_sub_ajax/', views.add_sub_ajax, name='add_sub_ajax'),
    path('test_auth/', views.test_auth, name='test_auth'),



]
