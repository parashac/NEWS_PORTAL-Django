from django.contrib import admin
from news_app.models import Post, Category, Tag, Advertisement, Contact, OurTeam, UserProfile, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Advertisement)
admin.site.register(Contact)
admin.site.register(OurTeam)
admin.site.register(UserProfile)
admin.site.register(Comment)
