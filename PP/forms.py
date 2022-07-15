from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post, Comment

class UserLoginForm(AuthenticationForm):
	username = forms.CharField(label='', max_length=20, widget=forms.TextInput(attrs={'class':'login_input', 'placeholder': 'Имя пользователя'}))
	password = forms.CharField(label='', max_length=30, widget=forms.PasswordInput(attrs={'class':'login_input', 'placeholder': 'Пароль'}))

class RegisterForm(UserCreationForm):
	username = forms.CharField(label='', max_length=20, widget=forms.TextInput(attrs={'class':'reg_input', 'placeholder': 'Имя пользователя'}))
	email = forms.EmailField(label='', max_length=320, widget=forms.EmailInput(attrs={'class':'reg_input', 'placeholder': 'Электронная почта'}))
	password1 = forms.CharField(label='', max_length=30, widget=forms.PasswordInput(attrs={'class':'reg_input', 'placeholder': 'Пароль'}))
	password2 = forms.CharField(label='', max_length=30, widget=forms.PasswordInput(attrs={'class':'reg_input', 'placeholder': 'Повторите пароль'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2', )

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['content', 'author',]
		widgets = {
			'content': forms.Textarea(attrs={'class': 'post_input', 'placeholder': 'Поделитесь чем-нибудь с нами!'}),
			'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'name', 'type': 'hidden',})
		}

	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['content'].label = ''

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['post', 'comment_text', 'author']
		widgets = {
			'post': forms.TextInput(attrs={'class': 'comment_input', 'value': '', 'id': 'post', 'type': 'hidden',}),
			'comment_text': forms.Textarea(attrs={'class': 'comment_input', 'autofocus': 'on', 'placeholder': 'Напишите комментарий'}),
			'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'author', 'type': 'hidden',})
		}
		
	def __init__(self, *args, **kwargs):
		super(CommentForm, self).__init__(*args, **kwargs)
		self.fields['comment_text'].label = ''
