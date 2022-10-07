from django.contrib import admin

from .models import Post, Comment, Profile, PostImage

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(PostImage)
