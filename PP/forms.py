from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Profile

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
			'bio': forms.TextInput(attrs={'class': 'bio_input', 'id': 'bio_input',}),			
			'first_name': forms.TextInput(attrs={'class': 'first_name_input', 'id': 'first_name_input',}),
			'last_name': forms.TextInput(attrs={'class': 'last_name_input', 'id': 'last_name_input',}),
			'sex': forms.Select(attrs={'class': 'select', 'id': 'select',}),
			'link1': forms.URLInput(attrs={'class': 'vk_url', 'id': 'vk_url',}),
			'link2': forms.URLInput(attrs={'class': 'inst_url', 'id': 'inst_url',}),
			'link3': forms.URLInput(attrs={'class': 'tg_url', 'id': 'tg_url',}),
			'link4': forms.URLInput(attrs={'class': 'tiktok_url', 'id': 'tiktok_url',}),
		}


#class UserProfileForm(forms.Form):
	#username = forms.CharField(label='Username', max_length=30)
	#email = forms.EmailField(label='E-mail', max_length=255)
	#profile_pic = forms.ImageField(label='Profile Picture')
	#bio = forms.CharField(label='io', max_length=300)
	#birthdate = forms.DateField()
	#city = forms.CharField(label='City', max_length=100)
	#first_name = forms.CharField(label='First name', max_length=50)
	#last_name = forms.CharField(label='Last name', max_length=50)
	#sex = forms.ChoiceField(label='Sex', choices=SEX_CHOICES)
	#link1 = forms.URLField(label='VK')
	#link2 = forms.URLField(label='Instagram')
	#link3 = forms.URLField(label='Telegram')
	#link4 = forms.URLField(label='TikTok')

	#class Meta:
		#fields = ['username', 'email']
		#widgets = {
		#	'username': forms.TextInput(attrs={'class': 'username_input', 'id': 'username_input',}),
		#	'email': forms.TextInput(attrs={'class': 'email_input', 'id': 'email_input',}),
		#}








