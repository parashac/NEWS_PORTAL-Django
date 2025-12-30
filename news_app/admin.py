from django.contrib import admin
from news_app.models import Post, Category ,Tag
# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)