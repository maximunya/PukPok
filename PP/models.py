from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500)
	profile_pic = models.ImageField(null=True, blank=True, upload_to="profile-images/",)
	link1 = models.CharField(max_length=300, null=True, blank=True,)
	link2 = models.CharField(max_length=300, null=True, blank=True,)
	link3 = models.CharField(max_length=300, null=True, blank=True,)
	link4 = models.CharField(max_length=300, null=True, blank=True,)

	def __str__(self):
		return str(self.user)


class Post(models.Model):
	author = models.ForeignKey(User, blank=False, default=1, on_delete=models.CASCADE)
	content = models.TextField(max_length=1000)
	posted_at = models.DateTimeField(auto_now_add=True)
	edited_at = models.DateTimeField(auto_now=True)
	is_published = models.BooleanField(default=True)
	likes = models.ManyToManyField(User, blank=True, related_name='blog_posts')
	total_likes = models.IntegerField(default=0)


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

	def total_likes(self):
		return self.likes.count()

	def __str__(self):
		return self.comment_text

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'
		ordering = ['-comment_posted_at']