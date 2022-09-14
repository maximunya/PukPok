from django.urls import path
from . import views
from .views import ProfilePage, CreatePostForm, CreateCommentForm, PostDetailView
from .views import UpdatePostView, UpdateCommentView, UpdateProfileView, UpdateUserView
from rest_framework.routers import SimpleRouter


urlpatterns = [
	path('', views.index, name = 'index'),
	path('register', views.register, name = 'register'),
	path('login', views.login, name = 'login'),
	path('logout', views.user_logout, name = 'logout'),
	path('like/<int:pk>', views.like, name='like_post'),
	path('like_comment/<int:pk>', views.like_comment, name='like_comment'),
	path('user/<int:pk>', ProfilePage.as_view(), name='profile_page'),
	path('create_post', CreatePostForm.as_view(), name='create_post'),
	path('create_comment', CreateCommentForm.as_view(), name='create_comment'),
	path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
	path('friends', views.friends, name='friends'),
	path('post/<int:pk>/edit', UpdatePostView.as_view(), name='update_post'),
	path('post/<post_id>/delete', views.delete_post, name = 'delete_post'),
	path('post/<post_id>/remove', views.delete_post_profile, name = 'delete_post_profile'),
	path('comment/<int:pk>/edit', UpdateCommentView.as_view(), name='update_comment'),
	path('post/<post_id>/comment/<comment_id>/delete', views.delete_comment, name = 'delete_comment'),
	path('post/<post_id>/comment/<comment_id>/remove', views.delete_comment_profile, name = 'delete_comment_profile'),
	path('user/<int:pk>/edit_profile', UpdateProfileView.as_view(), name='edit_profile'),
	path('user/<int:pk>/user_settings', UpdateUserView.as_view(), name='user_settings'),
	path('user/<int:pk>/delete', views.delete_user, name="delete_user"),
]

