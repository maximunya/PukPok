from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from django.utils import timezone as tz

class Profile(models.Model):
	SEX_CHOICES = [
		('Мужской', 'Мужской'),
		('Женский', 'Женский'),
	]

	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500)
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