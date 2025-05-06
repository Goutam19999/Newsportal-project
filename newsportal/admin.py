from django.contrib import admin

from newsportal.models import Category, Comment, Contact, NewsLetter, Post, Tag, UserProfile

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(NewsLetter)
admin.site.register(UserProfile)
