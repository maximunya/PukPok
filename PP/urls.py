from django.urls import path
from . import views
from .views import ProfilePage, CreateCommentForm, PostDetailView
from .views import UpdatePostView, UpdateCommentView, UpdateProfilePicView, UpdateProfileView, UpdateUserView
from rest_framework.routers import SimpleRouter


urlpatterns = [
	path('', views.index, name = 'index'),
	path('register', views.register, name = 'register'),
	path('login', views.login, name = 'login'),
	path('logout', views.user_logout, name = 'logout'),
	path('like/<int:pk>', views.like, name='like_post'),
	path('like_comment/<int:pk>', views.like_comment, name='like_comment'),
	path('user/<int:pk>', ProfilePage.as_view(), name='profile_page'),
	path('create_comment', CreateCommentForm.as_view(), name='create_comment'),
	path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
	path('post/<int:pk>/edit', UpdatePostView.as_view(), name='update_post'),
	path('post/<post_id>/delete', views.delete_post, name = 'delete_post'),
	path('post/<post_id>/remove', views.delete_post_profile, name = 'delete_post_profile'),
	path('comment/<int:pk>/edit', UpdateCommentView.as_view(), name='update_comment'),
	path('post/<post_id>/comment/<comment_id>/delete', views.delete_comment, name = 'delete_comment'),
	path('post/<post_id>/comment/<comment_id>/remove', views.delete_comment_profile, name = 'delete_comment_profile'),
	path('user/<int:pk>/edit_profile_pic', UpdateProfilePicView.as_view(), name='edit_profile_pic'),
	path('user/<int:pk>/edit_profile', UpdateProfileView.as_view(), name='edit_profile'),
	path('user/<int:pk>/user_settings', UpdateUserView.as_view(), name='user_settings'),
	path('user/<int:pk>/delete', views.delete_user, name="delete_user"),
	path('subscribe/<int:pk>', views.subscribe, name='subscribe_profile'),
	path('test', views.test, name='test'),
	path('user/<int:pk>/subscribes', views.subscribes, name='subscribes_list'),
	path('user/<int:pk>/subscribers', views.subscribers, name='subscribers_list'),
	path('post/<int:pk>/likes', views.liked_post, name='liked_post_list'),
	path('comment/<int:pk>/likes', views.liked_comment, name='liked_comment_list'),
	path('notifications', views.notifications, name='notifications'),
	path('notifications/delete_notification/<int:pk>', views.delete_notification, name='delete_notification'),
	path('notifications/delete_all_notifications', views.delete_all_notifications, name='delete_all_notifications'),
	path('block/<int:pk>', views.add_user_to_black_list, name='block_user'),
	path('delete_sub/<int:pk>', views.delete_from_subscribers, name='delete_sub'),
	path('black_list', views.black_list, name='black_list'),
	path('users_list', views.users_list, name='users_list'),
	path('archived_posts', views.archived_posts_list, name='archived_posts'),
	path('post_to_archive/<int:pk>', views.post_to_archive, name='post_to_archive'),
]
