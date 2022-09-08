from django.contrib.auth.models import User
from PP.models import Profile

def update_user_profile(user, data: dict):
	#current_user = User.objects.get(id=user.id)
	current_profile = Profile.objects.get(user=user)

	user.username = data['user.username']
	user.email = data['user.email']

	user.save()

	current_profile.profile_pic = data['profile.profile_pic']
	current_profile.bio = data['profile.bio']
	current_profile.birthdate = data['profile.birthdate']
	current_profile.city = data['profile.city']
	current_profile.first_name = data['profile.first_name']
	current_profile.last_name = data['profile.last_name']
	current_profile.sex = data['profile.sex']
	current_profile.link1 = data['profile.link1']
	current_profile.link2 = data['profile.link2']
	current_profile.link3 = data['profile.link3']
	current_profile.link4 = data['profile.link4']

	current_profile.save()

