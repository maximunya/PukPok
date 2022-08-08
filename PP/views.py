from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Profile
from .forms import RegisterForm, UserLoginForm, PostForm, CommentForm
from django.contrib.auth import login as auth_login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, FormView, UpdateView
from django.views.generic.edit import ModelFormMixin 
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
	posts = Post.objects.order_by('-posted_at')
	comments = Comment.objects.order_by('-comment_posted_at')
	context = {
		'posts': posts,
		'comments': comments,
		
	}
	return render(request, "PP/index.html", context)



class PostDetailView(DetailView):
	model = Post
	template_name = 'PP/post_detail.html'
	#success_url = reverse('post_detail', kwargs={'pk': self.object.id})

	def get_context_data(self, *args, **kwargs):
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



def user_logout(request):
	logout(request)
	return redirect('index')


@login_required
def like(request, pk):
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
	

def friends(request):
	return render(request, "PP/friends.html", )



class UpdatePostView(UpdateView):
	model = Post
	form_class = PostForm
	template_name = "PP/update_post.html"

	def get_success_url(self, **kwargs):
		messages.success(self.request, 'Пост изменён.')
		return reverse_lazy('post_detail', kwargs={'pk': self.object.id})
		#return redirect(self.request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def delete_post(request, post_id):
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
		#return redirect(self.request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required
def delete_comment(request, comment_id, post_id):
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
	comment = Comment.objects.get(pk=comment_id)
	post = Post.objects.get(pk=post_id)
	if request.user == post.author:
		comment.delete()
		messages.success(request, 'Комментарий удалён.')
		#return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
		return redirect(comment)
	elif request.user == comment.author:
		comment.delete()
		messages.success(request, 'Комментарий удалён.')
		#return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
		return redirect(comment)
	else:
		messages.error(request, 'Вы не можете удалить этот объект.')
		return redirect('index')

