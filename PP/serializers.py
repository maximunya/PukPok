from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'username',
			'email',
		)

	def __init__(self, *args, **kwargs):
		super(UserSerializer, self).__init__(*args, **kwargs)
		self.fields['username'].style.update({'template': 'PP/custom_input.html', 'class': 'form-control username_input', 'value': '', 'id': 'username',})
		self.fields['username'].help_text = ""
		self.fields['email'].style.update({'template': 'PP/custom_input.html', 'class': 'form-control email_input', 'value': '', 'id': 'email',})
		self.fields['email'].label = 'Адрес эл. почты'
		self.label = ""


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = (
			'profile_pic', 'bio', 'birthdate', 'city',
			'first_name', 'last_name', 'sex',
			'link1', 'link2', 'link3', 'link4',
		)

	def __init__(self, *args, **kwargs):
		super(ProfileSerializer, self).__init__(*args, **kwargs)
		self.fields['profile_pic'].style.update({'template': 'PP/custom_input.html', 'class': 'profile_pic_input', 'value': '', 'id': 'profile_pic',})
		self.fields['bio'].style.update({'template': 'PP/custom_input.html', 'class': 'form-control bio_input', 'value': '', 'id': 'bio',})
		self.fields['birthdate'].style.update({'template': 'PP/custom_input.html', 'class': '', 'id': 'birthdate', 'input_type': 'date',})
		self.fields['city'].style.update({'template': 'PP/custom_input.html', 'class': 'form-control city_input', 'value': '', 'id': 'city',})
		self.fields['first_name'].style.update({'template': 'PP/custom_input.html', 'class': 'form-control first_name_input', 'value': '', 'id': 'first_name',})
		self.fields['last_name'].style.update({'template': 'PP/custom_input.html', 'class': 'form-control last_name_input', 'value': '', 'id': 'last_name',})
		self.fields['sex'].style.update({'template': 'PP/custom_select.html', 'class': 'form-control sex_input', 'value': '', 'id': 'sex',})
		self.fields['link1'].style.update({'template': 'PP/custom_input.html', 'class': 'form-control vk_input', 'value': '', 'id': 'vk',})
		self.fields['link2'].style.update({'template': 'PP/custom_input.html', 'class': 'form-control inst_input', 'value': '', 'id': 'inst',})
		self.fields['link3'].style.update({'template': 'PP/custom_input.html', 'class': 'form-control telegram_input', 'value': '', 'id': 'telegram',})
		self.fields['link4'].style.update({'template': 'PP/custom_input.html', 'class': 'form-control tiktok_input', 'value': '', 'id': 'tiktok',})

		self.fields['profile_pic'].label = 'Картинка профиля'
		self.fields['bio'].label = 'О себе'
		self.fields['birthdate'].label = 'Дата рождения'
		self.fields['city'].label = 'Город'
		self.fields['first_name'].label = 'Имя'
		self.fields['last_name'].label = 'Фамилия'
		self.fields['sex'].label = 'Пол'
		self.fields['link1'].label = 'ВКонтакте'
		self.fields['link2'].label = 'Instagram'
		self.fields['link3'].label = 'Telegram'
		self.fields['link4'].label = 'TikTok'

		self.label = ""


class UserProfileSerializer(serializers.Serializer):
	user = UserSerializer()
	profile = ProfileSerializer()




