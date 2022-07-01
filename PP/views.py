from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Profile
from .forms import RegisterForm, UserLoginForm, PostForm
from django.contrib.auth import login as auth_login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, FormView


def index(request):
	posts = Post.objects.order_by('-posted_at')
	comments = Comment.objects.order_by('-comment_posted_at')
	context = {'posts': posts, 'comments': comments,}
	return render(request, "PP/index.html", context)

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			auth_login(request, user)
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

def user_logout(request):
	logout(request)
	return redirect('index')

def like(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	post.likes.add(request.user)
	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def like_comment(request, pk):
	comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
	comment.likes.add(request.user)
	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


class CreatePostForm(CreateView):
	form_class = PostForm
	template_name = 'PP/create_post.html'
	#success_url = redirect('profile_page')


class ProfilePage(DetailView):
	model = Profile 
	template_name = 'PP/profile_page.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ProfilePage, self).get_context_data(*args, **kwargs)
		posts = Post.objects.filter(author_id=self.kwargs['pk'])
		page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
		#context["form"] = AddPost
		context['create_post_form'] = PostForm()
		context["page_user"] = page_user
		context["posts"] = posts
		return context

	
	








