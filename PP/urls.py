from django.urls import path
from . import views
from .views import ProfilePage, CreatePostForm

urlpatterns = [
	path('', views.index, name = 'index'),
	path('register', views.register, name = 'register'),
	path('login', views.login, name = 'login'),
	path('logout', views.user_logout, name = 'logout'),
	path('like/<int:pk>', views.like, name='like_post'),
	path('like_comment/<int:pk>', views.like_comment, name='like_comment'),
	path('user/<int:pk>', ProfilePage.as_view(), name='profile_page'),
	path('create_post', CreatePostForm.as_view(), name='create_post'),
]