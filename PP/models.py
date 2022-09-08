from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta, datetime, date
from django.utils import timezone as tz
from django.utils import dateformat
import pytz

class Profile(models.Model):
	SEX_CHOICES = [
		('Мужской', 'Мужской'),
		('Женский', 'Женский'),
	]

	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500)
	birthdate = models.DateField(null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	profile_pic = models.ImageField(null=True, blank=True, upload_to="profile-images/",)
	sex = models.CharField(null=True, blank=True, max_length=7, choices=SEX_CHOICES)
	link1 = models.CharField(max_length=300, null=True, blank=True,)
	link2 = models.CharField(max_length=300, null=True, blank=True,)
	link3 = models.CharField(max_length=300, null=True, blank=True,)
	link4 = models.CharField(max_length=300, null=True, blank=True,)

	def __str__(self):
		return str(self.user)



@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)


class Post(models.Model):
	author = models.ForeignKey(User, blank=False, default=1, on_delete=models.CASCADE)
	content = models.TextField(max_length=3000)
	posted_at = models.DateTimeField(auto_now_add=True)
	edited_at = models.DateTimeField(auto_now=True)
	is_published = models.BooleanField(default=True)
	likes = models.ManyToManyField(User, blank=True, related_name='blog_posts')
	total_likes = models.IntegerField(default=0)
	#total_comments = models.IntegerField(default=0)

	def test(self):
		now = datetime.now(pytz.timezone('Europe/Moscow'))
		lst = now.strftime('%Y-%m-%d').split("-")
		date = int(lst[2])
		month = int(lst[1])
		year = int(lst[0])
		return date

	def test1(self):
		pub_date = tz.localtime(self.posted_at)
		lst = dateformat.format(pub_date, 'Y-m-d').split("-")
		lst1 = lst[2].split()
		date = int(lst1[0])
		month = int(lst[1])
		year = int(lst[0])
		return lst

	def mytime(self):
		if tz.now() < self.posted_at + timedelta(seconds=10):
			return 'Только что'
		elif tz.now() < self.posted_at + timedelta(seconds=20):
			return '10 секунд назад'
		elif tz.now() < self.posted_at + timedelta(seconds=30):
			return '20 секунд назад'
		elif tz.now() < self.posted_at + timedelta(seconds=40):
			return '30 секунд назад'
		elif tz.now() < self.posted_at + timedelta(seconds=50):
			return '40 секунд назад'
		elif tz.now() < self.posted_at + timedelta(seconds=60):
			return '50 секунд назад'
		elif tz.now() < self.posted_at + timedelta(minutes=2):
			return 'минуту назад'
		elif tz.now() < self.posted_at + timedelta(minutes=3):
			return '2 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=4):
			return '3 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=5):
			return '4 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=6):
			return '5 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=7):
			return '6 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=8):
			return '7 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=9):
			return '8 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=10):
			return '9 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=11):
			return '10 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=12):
			return '11 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=13):
			return '12 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=14):
			return '13 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=15):
			return '14 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=16):
			return '15 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=17):
			return '16 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=18):
			return '17 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=19):
			return '18 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=20):
			return '19 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=21):
			return '20 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=22):
			return '21 минуту назад'
		elif tz.now() < self.posted_at + timedelta(minutes=23):
			return '22 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=24):
			return '23 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=25):
			return '24 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=26):
			return '25 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=27):
			return '26 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=28):
			return '27 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=29):
			return '28 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=30):
			return '29 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=31):
			return '30 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=32):
			return '31 минуту назад'
		elif tz.now() < self.posted_at + timedelta(minutes=33):
			return '32 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=34):
			return '33 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=35):
			return '34 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=36):
			return '35 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=37):
			return '36 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=38):
			return '37 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=39):
			return '38 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=40):
			return '39 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=41):
			return '40 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=42):
			return '41 минуту назад'
		elif tz.now() < self.posted_at + timedelta(minutes=43):
			return '42 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=44):
			return '43 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=45):
			return '44 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=46):
			return '45 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=47):
			return '46 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=48):
			return '47 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=49):
			return '48 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=50):
			return '49 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=51):
			return '50 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=52):
			return '51 минуту назад'
		elif tz.now() < self.posted_at + timedelta(minutes=53):
			return '52 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=54):
			return '53 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=55):
			return '54 минуты назад'
		elif tz.now() < self.posted_at + timedelta(minutes=56):
			return '55 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=57):
			return '56 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=58):
			return '57 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=59):
			return '58 минут назад'
		elif tz.now() < self.posted_at + timedelta(minutes=60):
			return '59 минут назад'
		elif tz.now() < self.posted_at + timedelta(hours=2):
			return 'час назад'
		elif tz.now() < self.posted_at + timedelta(hours=3):
			return '2 часа назад'
		elif tz.now() < self.posted_at + timedelta(hours=4):
			return '3 часа назад'

	def mytime1(self):

		now = datetime.now(pytz.timezone('Europe/Moscow'))
		lst = now.strftime('%Y-%m-%d').split("-")
		date = int(lst[2])
		month = int(lst[1])
		year = int(lst[0])

		pub_date = tz.localtime(self.posted_at)
		lst1 = dateformat.format(pub_date, 'Y-m-d').split("-")
		date1 = int(lst1[2])
		month1 = int(lst1[1])
		year1 = int(lst1[0])

		if tz.now() < self.posted_at + timedelta(hours=4): 
			return self.mytime()
		elif date == date1 and month == month1 and year == year1:
			return 1
		elif date - 1 == date1 and month == month1 and year == year1:
			return 2
		elif date - 2 == date1 and month == month1 and year == year1:
			return 3
		elif year == year1:
			return 4
		elif year > year1:
			return 5


	def total_comments(self):
		if self.comments.count() <= 10:
			if self.comments.count() == 1:
				return "комментарий"
			elif self.comments.count() in [2, 3, 4]:
				return "комментария"
			else:
				return "комментариев"
		elif self.comments.count() > 10 and self.comments.count() < 100:
			if self.comments.count() % 10 == 1 and self.comments.count() != 11:
				return "комментарий"
			elif self.comments.count() % 10 in [2, 3, 4] and self.comments.count() not in [12, 13, 14]:
				return "комментария"
			else:
				return "комментариев"
		else:
			if self.comments.count() % 10 == 1 and self.comments.count() % 100 != 11:
				return "комментарий"
			elif self.comments.count() % 10 in [2, 3, 4] and self.comments.count() % 100 not in [12, 13, 14]:
				return "комментария"
			else:
				return "комментариев"

	def can_edit(self):
		if tz.now() < self.posted_at + timedelta(days=1):
			return True
		else:
			return False

	def total_likes(self):
		return self.likes.count()

	def __str__(self):
		return self.content

	def get_absolute_url(self):
		return reverse('profile_page', kwargs={'pk': self.author.pk})

	class Meta:
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'
		ordering = ['-posted_at']

class Comment(models.Model):
	author = models.ForeignKey(User, blank=False, default=1, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	comment_text = models.CharField(max_length=300)
	comment_posted_at = models.DateTimeField(auto_now_add=True)
	comment_edited_at = models.DateTimeField(auto_now=True)
	is_published = models.BooleanField(default=True)
	likes = models.ManyToManyField(User, blank=True, related_name='blog_comments')
	total_likes = models.IntegerField(default=0)

	def с_mytime(self):
		if tz.now() < self.comment_posted_at + timedelta(seconds=10):
			return 'Только что'
		elif tz.now() < self.comment_posted_at + timedelta(seconds=20):
			return '10 секунд назад'
		elif tz.now() < self.comment_posted_at + timedelta(seconds=30):
			return '20 секунд назад'
		elif tz.now() < self.comment_posted_at + timedelta(seconds=40):
			return '30 секунд назад'
		elif tz.now() < self.comment_posted_at + timedelta(seconds=50):
			return '40 секунд назад'
		elif tz.now() < self.comment_posted_at + timedelta(seconds=60):
			return '50 секунд назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=2):
			return 'минуту назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=3):
			return '2 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=4):
			return '3 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=5):
			return '4 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=6):
			return '5 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=7):
			return '6 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=8):
			return '7 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=9):
			return '8 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=10):
			return '9 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=11):
			return '10 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=12):
			return '11 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=13):
			return '12 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=14):
			return '13 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=15):
			return '14 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=16):
			return '15 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=17):
			return '16 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=18):
			return '17 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=19):
			return '18 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=20):
			return '19 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=21):
			return '20 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=22):
			return '21 минуту назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=23):
			return '22 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=24):
			return '23 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=25):
			return '24 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=26):
			return '25 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=27):
			return '26 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=28):
			return '27 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=29):
			return '28 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=30):
			return '29 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=31):
			return '30 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=32):
			return '31 минуту назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=33):
			return '32 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=34):
			return '33 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=35):
			return '34 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=36):
			return '35 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=37):
			return '36 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=38):
			return '37 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=39):
			return '38 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=40):
			return '39 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=41):
			return '40 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=42):
			return '41 минуту назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=43):
			return '42 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=44):
			return '43 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=45):
			return '44 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=46):
			return '45 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=47):
			return '46 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=48):
			return '47 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=49):
			return '48 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=50):
			return '49 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=51):
			return '50 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=52):
			return '51 минуту назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=53):
			return '52 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=54):
			return '53 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=55):
			return '54 минуты назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=56):
			return '55 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=57):
			return '56 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=58):
			return '57 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=59):
			return '58 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(minutes=60):
			return '59 минут назад'
		elif tz.now() < self.comment_posted_at + timedelta(hours=2):
			return 'час назад'
		elif tz.now() < self.comment_posted_at + timedelta(hours=3):
			return '2 часа назад'
		elif tz.now() < self.comment_posted_at + timedelta(hours=4):
			return '3 часа назад'

	def с_mytime1(self):

		now = datetime.now(pytz.timezone('Europe/Moscow'))
		lst = now.strftime('%Y-%m-%d').split("-")
		date = int(lst[2])
		month = int(lst[1])
		year = int(lst[0])

		pub_date = tz.localtime(self.comment_posted_at)
		lst1 = dateformat.format(pub_date, 'Y-m-d').split("-")
		date1 = int(lst1[2])
		month1 = int(lst1[1])
		year1 = int(lst1[0])

		if tz.now() < self.comment_posted_at + timedelta(hours=4): 
			return self.с_mytime()
		elif date == date1 and month == month1 and year == year1:
			return 1
		elif date - 1 == date1 and month == month1 and year == year1:
			return 2
		elif date - 2 == date1 and month == month1 and year == year1:
			return 3
		elif year == year1:
			return 4
		elif year > year1:
			return 5

	def can_edit(self):
		if tz.now() < self.comment_posted_at + timedelta(days=1):
			return True
		else:
			return False


	def total_likes(self):
		return self.likes.count()

	def __str__(self):
		return self.comment_text

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk': self.post.pk})


	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'
		ordering = ['-comment_posted_at']