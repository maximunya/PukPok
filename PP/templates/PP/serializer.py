from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'id',
			'username',
			'email',
		)


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = (
			'profile_pic', 'bio', 'birthdate', 'city',
			'first_name', 'last_name', 'sex',
			'link1', 'link2', 'link3', 'link4',
		)


class UserProfileSerializer(serializers.Serializer):
	#id = serializers.IntegerField()
	user = UserSerializer()
	profile = ProfileSerializer()
