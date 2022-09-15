from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Post, Comment, Profile
from ckeditor.widgets import CKEditorWidget
import re
from django.core.exceptions import ValidationError




SEX_CHOICES = [
		('Мужской', 'Мужской'),
		('Женский', 'Женский'),
	]

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
		#self.fields['content'].widget = CKEditorWidget()


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


class ProfileForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = [
			'profile_pic', 'bio', 'birthdate', 'city',
			'first_name', 'last_name', 'sex',
			'link1', 'link2', 'link3', 'link4',
		]
		widgets = {
			#'profile_pic': forms.FileInput(attrs={'class': 'profile_pic_input', 'id': 'profile_pic_input',}),
			'bio': forms.Textarea(attrs={'class': 'bio_input', 'id': 'bio_input',}),
			'birthdate': forms.TextInput(attrs={'class': 'birthdate_input', 'type': 'date', 'id': 'birthdate_input',}),			
			'first_name': forms.TextInput(attrs={'class': 'first_name_input', 'id': 'first_name_input',}),
			'last_name': forms.TextInput(attrs={'class': 'last_name_input', 'id': 'last_name_input',}),
			'sex': forms.Select(attrs={'class': 'select', 'id': 'select',}),
			'link1': forms.URLInput(attrs={'class': 'vk_url', 'id': 'vk_url',}),
			'link2': forms.URLInput(attrs={'class': 'inst_url', 'id': 'inst_url',}),
			'link3': forms.URLInput(attrs={'class': 'tg_url', 'id': 'tg_url',}),
			'link4': forms.URLInput(attrs={'class': 'tiktok_url', 'id': 'tiktok_url',}),
		}


	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['profile_pic'].label = 'Картинка профиля'
		self.fields['bio'].label = 'Био'
		self.fields['birthdate'].label = 'Дата рождения'
		self.fields['city'].label = 'Город'
		self.fields['first_name'].label = 'Имя'
		self.fields['last_name'].label = 'Фамилия'
		self.fields['sex'].label = 'Пол'
		self.fields['link1'].label = 'Вконтакте'
		self.fields['link2'].label = 'Instagram'
		self.fields['link3'].label = 'Telegram'
		self.fields['link4'].label = 'TikTok'


regex1 = r"^[a-z0-9_.]+$"
regex2 = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def valid_username(strg):
	if re.fullmatch(regex1, strg):
		return True
	else:
		return False

def valid_email(strg):
	if re.fullmatch(regex2, strg):
		return True
	else:
		return False


class UserUpdateForm(UserChangeForm):

	class Meta:
		model = User
		fields = ['username', 'email',]

	def __init__(self, *args, **kwargs):
		super(UserUpdateForm, self).__init__(*args, **kwargs)
		self.fields['email'].label = 'Электронная почта'
		#self.fields['password'].label = ''
		self.fields['username'].help_text = ''
		self.fields['password'].help_text = ''

	def clean(self):
		cleaned_data = super(UserUpdateForm, self).clean()
		username = cleaned_data.get('username')
		email = cleaned_data.get('email')
		if username is not None and email is not None:
			if not valid_username(username):
				self.add_error(None, ValidationError('Имя пользователя может состоять только из латинницы, цифр и символов -_.'))
			if not valid_email(email):
				self.add_error(None, ValidationError('Указан неверный адрес электронной почты'))









