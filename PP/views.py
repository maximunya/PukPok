from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Profile
from .forms import RegisterForm, UserLoginForm, PostForm, CommentForm, ProfileForm, ProfilePicForm, UserUpdateForm, PostImagesForm
from django.contrib.auth import login as auth_login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, FormView, UpdateView
from django.views.generic.edit import ModelFormMixin 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserProfileSerializer, ProfileSerializer
from .services.update import update_user_profile
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions
from datetime import datetime, timedelta




class LoggedAndPassedTestUserMixin(LoginRequiredMixin, UserPassesTestMixin):

	def test_func(self):
		return self.request.user.id == self.kwargs['pk']

	def handle_no_permission(self):
		messages.error(self.request, 'Ошибка доступа')
		return redirect('index')


class LoggedAndPassedTestProfileMixin(LoginRequiredMixin, UserPassesTestMixin):

	def test_func(self):
		return self.request.user.profile.id == self.kwargs['pk']

	def handle_no_permission(self):
		messages.error(self.request, 'Ошибка доступа')
		return redirect('index')


class LoggedAndPassedTestPostMixin(LoginRequiredMixin, UserPassesTestMixin):

	def test_func(self):
		post = Post.objects.get(id=self.kwargs['pk'])
		return self.request.user.id == post.author.id

	def handle_no_permission(self):
		messages.error(self.request, 'Ошибка доступа')
		return redirect('index')


#class UpdateUserProfileAPI(viewsets.GenericViewSet):

	#renderer_classes = [TemplateHTMLRenderer,]
	#template_name = 'PP/update_user_info.html'
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

	#def get_queryset(self):
	#	queryset = Profile.objects.all()
	#	return queryset

	#def get_serializer_class(self):
	#	return UserProfileSerializer

	#@action(methods=["GET",], detail=False)
	#def get(self, request):
	#	return Response({'serializer': self.get_serializer_class(),},)

	#@action(methods=["POST",], detail=False)
	#def post(self, request):
	#	user = request.user
	#	data = request.data
	#	update_user_profile(user=user, data=data)
	#	return Response({'serializer': self.get_serializer_class(),},)

	#@action(methods=["PUT",], detail=False)
	#def edit_profile(self, request, *args, **kwargs):
	#	user = request.user
	#	data = request.data
	#	update_user_profile(user=user, data=data)
	#	return Response({'serializer': self.get_serializer_class(),},)

	#def get_success_url(self, **kwargs):
		#return reverse_lazy('profile_page', kwargs={'pk': self.request.user.id})

	
def index(request):
	if request.user.is_authenticated:
		user = User.objects.select_related('profile').get(pk=request.user.id)
		user.profile.last_active = datetime.now()
		user.save()
	posts = Post.objects.prefetch_related('comments__author__profile').select_related('author__profile').prefetch_related("likes").prefetch_related('comments__likes').prefetch_related('post_images').filter(is_published=True)
	context = {
		'posts': posts,
	}
	return render(request, "PP/index.html", context)


def test(request):
	posts = Post.objects.prefetch_related('comments__author__profile').select_related('author__profile').prefetch_related("likes").prefetch_related('comments__likes').all()
	context = {
		'posts': posts,
	}
	return render(request, 'PP/test.html', context)


class PostDetailView(DetailView):
	model = Post
	template_name = 'PP/post_detail.html'

	def get_context_data(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			user = User.objects.get(pk=self.request.user.id)
			user.profile.last_active = datetime.now()
			user.save()
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)
		post = get_object_or_404(Post, id=self.kwargs['pk'])
		context['create_comment_form'] = CommentForm()
		context["post"] = post
		return context


class CreateCommentForm(CreateView):
	form_class = CommentForm
	template_name = 'PP/create_comment.html'


def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			auth_login(request, user)
			messages.success(request, 'Вы успешно зарегистрировались!')
			return redirect('index')
	else:
		form = RegisterForm()
	return render(request, "PP/register.html", {"form": form})


def login(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			auth_login(request, user)
			return redirect('index')
	else:
		form = UserLoginForm()
	return render(request, "PP/login.html", {'form': form})


@login_required
def user_logout(request):
	logout(request)
	return redirect('index')


@login_required
def like(request, pk):
	if request.user.is_authenticated:
		user = User.objects.get(pk=request.user.id)
		user.profile.last_active = datetime.now()
		user.save()
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True

	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def like_comment(request, pk):
	if request.user.is_authenticated:
		user = User.objects.get(pk=request.user.id)
		user.profile.last_active = datetime.now()
		user.save()
	comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
	liked = False
	if comment.likes.filter(id=request.user.id).exists():
		comment.likes.remove(request.user)
		liked = False
	else:
		comment.likes.add(request.user)
		liked = True

	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


class CreatePostForm(CreateView):
	form_class = PostForm
	template_name = 'PP/create_post.html'


class ProfilePage(DetailView):
	model = Profile 
	template_name = 'PP/profile_page.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ProfilePage, self).get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated:
			user = User.objects.select_related("profile").get(pk=self.request.user.id)
			user.profile.last_active = datetime.now()
			user.save()

		profile = Profile.objects.get(id=self.kwargs['pk'])
		user_id = profile.user_id
		
		posts = Post.objects.prefetch_related('comments__author__profile').select_related('author__profile').prefetch_related("likes").prefetch_related('comments__likes').filter(author_id=user_id).filter(is_published=True)
		posts_amount = posts.count()
		subscribers_amount = profile.subscribers.count()
		subs_amount = Profile.objects.select_related('user').filter(subscribers=user_id).count()

		if posts_amount <= 10:
			if posts_amount == 1:
				total_posts = f"{posts_amount} пост"
			elif posts_amount in [2, 3, 4]:
				total_posts = f"{posts_amount} поста"
			else:
				total_posts = f"{posts_amount} постов"
		elif posts_amount > 10 and posts_amount < 100:
			if posts_amount % 10 == 1 and posts_amount != 11:
				total_posts = f"{posts_amount} пост"
			elif posts_amount % 10 in [2, 3, 4] and posts_amount not in [12, 13, 14]:
				total_posts = f"{posts_amount} поста"
			else:
				total_posts = f"{posts_amount} постов"
		else:
			if posts_amount % 10 == 1 and posts_amount % 100 != 11:
				total_posts = f"{posts_amount} пост"
			elif posts_amount % 10 in [2, 3, 4] and posts_amount % 100 not in [12, 13, 14]:
				total_posts = f"{posts_amount} поста"
			else:
				total_posts = f"{posts_amount} постов"
		page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
		context['create_post_form'] = PostForm()
		context['post_images_form'] = PostImagesForm()
		context["page_user"] = page_user
		context["posts"] = posts
		context['total_posts'] = total_posts
		context['subscribers_amount'] = subscribers_amount
		context['subs_amount'] = subs_amount
		return context
	

def subscribes(request, pk):
	if request.user.is_authenticated:
		user = User.objects.select_related("profile").get(pk=request.user.id)
		user.profile.last_active = datetime.now()
		user.save()

	profile = Profile.objects.select_related('user').get(id=pk)
	my_subs = Profile.objects.select_related('user').filter(subscribers=profile.user.id)

	context = {
		'my_subs': my_subs,
		'profile': profile,
	}
	return render(request, "PP/subscribes.html", context)


def subscribers(request, pk):
	if request.user.is_authenticated:
		user = User.objects.select_related("profile").get(pk=request.user.id)
		user.profile.last_active = datetime.now()
		user.save()

	profile = Profile.objects.prefetch_related("subscribers").select_related('user').get(id=pk)
	subscribers = profile.subscribers.select_related('profile').all()

	context = {
		'profile': profile,
		'subscribers': subscribers,
	}
	return render(request, "PP/subscribers.html", context)


def liked_post(request, pk):
	if request.user.is_authenticated:
		user = User.objects.select_related("profile").get(pk=request.user.id)
		user.profile.last_active = datetime.now()
		user.save()
	post = Post.objects.prefetch_related("likes").select_related('author').get(id=pk)
	users_liked = post.likes.select_related('profile').all()
	context = {
		'users_liked': users_liked,
	}
	return render(request, "PP/liked_post.html", context)


def liked_comment(request, pk):
	if request.user.is_authenticated:
		user = User.objects.select_related("profile").get(pk=request.user.id)
		user.profile.last_active = datetime.now()
		user.save()
	comment = Comment.objects.prefetch_related("likes").select_related('author').get(id=pk)
	users_liked = comment.likes.select_related('profile').all()
	context = {
		'users_liked': users_liked,
	}
	return render(request, "PP/liked_comment.html", context)


class UpdatePostView(LoggedAndPassedTestPostMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = "PP/update_post.html"

	def get_context_data(self, *args, **kwargs):
		context = super(UpdatePostView, self).get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated:
			user = User.objects.get(pk=self.request.user.id)
			user.profile.last_active = datetime.now()
			user.save()
		return context

	def get_success_url(self, **kwargs):
		messages.success(self.request, 'Пост изменён.')
		return reverse_lazy('post_detail', kwargs={'pk': self.object.id})


class UpdateProfilePicView(LoggedAndPassedTestProfileMixin, UpdateView):
	model = Profile
	form_class = ProfilePicForm
	template_name = 'PP/edit_profile_pic.html'

	def get_context_data(self, *args, **kwargs):
		context = super(UpdateProfilePicView, self).get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated:
			user = User.objects.get(pk=self.request.user.id)
			user.profile.last_active = datetime.now()
			user.save()
		return context

	def get_success_url(self, **kwargs):
		messages.success(self.request, 'Информация профиля изменена.')
		return reverse_lazy('profile_page', kwargs={'pk': self.request.user.profile.id})


class UpdateProfileView(LoggedAndPassedTestProfileMixin, UpdateView):
	model = Profile
	form_class = ProfileForm
	template_name = 'PP/edit_profile.html'

	def get_context_data(self, *args, **kwargs):
		context = super(UpdateProfileView, self).get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated:
			user = User.objects.get(pk=self.request.user.id)
			user.profile.last_active = datetime.now()
			user.save()
		return context

	def get_success_url(self, **kwargs):
		messages.success(self.request, 'Информация профиля изменена.')
		return reverse_lazy('profile_page', kwargs={'pk': self.request.user.profile.id})


class UpdateUserView(LoggedAndPassedTestUserMixin, UpdateView):
	model = User
	form_class = UserUpdateForm
	template_name = 'PP/user_settings.html'

	def get_context_data(self, *args, **kwargs):
		context = super(UpdateUserView, self).get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated:
			user = User.objects.get(pk=self.request.user.id)
			user.profile.last_active = datetime.now()
			user.save()
		return context

	def get_success_url(self, **kwargs):
		messages.success(self.request, 'Данные вашего аккаунта изменены.')
		return reverse_lazy('profile_page', kwargs={'pk': self.request.user.profile.id})


@login_required
def delete_post(request, post_id):
	if request.user.is_authenticated:
		user = User.objects.get(pk=request.user.id)
		user.profile.last_active = datetime.now()
		user.save()
	post = Post.objects.get(pk=post_id)
	if request.user == post.author:
		post.delete()
		messages.success(request, 'Пост удалён.')
		return redirect('index')
	else:
		messages.error(request, 'Вы не можете удалить этот объект.')
		return redirect('index')


@login_required
def delete_post_profile(request, post_id):
	if request.user.is_authenticated:
		user = User.objects.get(pk=request.user.id)
		user.profile.last_active = datetime.now()
		user.save()
	post = Post.objects.get(pk=post_id)
	if request.user == post.author:
		post.delete()
		messages.success(request, 'Пост удалён.')
		return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
	else:
		messages.error(request, 'Вы не можете удалить этот объект.')
		return redirect('index')


class UpdateCommentView(UpdateView):
	model = Comment
	form_class = CommentForm
	template_name = "PP/update_comment.html"
	
	def get_context_data(self, *args, **kwargs):
		context = super(UpdateCommentView, self).get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated:
			user = User.objects.get(pk=self.request.user.id)
			user.profile.last_active = datetime.now()
			user.save()
		str_url = str(self.request.path)
		splitted = str_url.split("/")
		com_id = int(splitted[2])
		context["splitted"] = splitted
		context["com_id"] = com_id
		context["str_url"] = str_url
		return context

	def get_success_url(self, **kwargs):
		messages.success(self.request, 'Комментарий изменён.')
		return reverse_lazy('post_detail', kwargs={'pk': self.object.post.id})


@login_required
def delete_comment(request, comment_id, post_id):
	if request.user.is_authenticated:
		user = User.objects.get(pk=request.user.id)
		user.profile.last_active = datetime.now()
		user.save()
	comment = Comment.objects.get(pk=comment_id)
	post = Post.objects.get(pk=post_id)
	if request.user == post.author:
		comment.delete()
		messages.success(request, 'Комментарий удалён.')
		return redirect('index')
	elif request.user == comment.author:
		comment.delete()
		messages.success(request, 'Комментарий удалён.')
		return redirect('index')
	else:
		messages.error(request, 'Вы не можете удалить этот объект.')
		return redirect('index')


@login_required
def delete_comment_profile(request, comment_id, post_id):
	if request.user.is_authenticated:
		user = User.objects.get(pk=request.user.id)
		user.profile.last_active = datetime.now()
		user.save()
	comment = Comment.objects.get(pk=comment_id)
	post = Post.objects.get(pk=post_id)
	if request.user == post.author:
		comment.delete()
		messages.success(request, 'Комментарий удалён.')
		return redirect(comment)
	elif request.user == comment.author:
		comment.delete()
		messages.success(request, 'Комментарий удалён.')
		return redirect(comment)
	else:
		messages.error(request, 'Вы не можете удалить этот объект.')
		return redirect('index')


@login_required
def delete_user(request, pk):
	if request.user.id == pk:
		request.user.delete()
		messages.success(request, 'Аккаунт удалён.')
		return redirect('index')
	else:
		messages.error(request, 'Вы не можете удалить этот объект.')
		return redirect('index')


@login_required
def subscribe(request, pk):
	if request.user.is_authenticated:
		user = User.objects.get(pk=request.user.id)
		user.profile.last_active = datetime.now()
		user.save()
	profile = get_object_or_404(Profile, id=request.POST.get('profile_id'))
	if request.user.id != pk:
		subscribed = False
		if profile.subscribers.filter(id=request.user.id).exists():
			profile.subscribers.remove(request.user)
			subscribed = False
		else:
			profile.subscribers.add(request.user)
			subscribed = True

	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

