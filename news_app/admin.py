from django.contrib import admin
from tinymce.widgets import TinyMCE

from news_app.models import Post, Category, Tag, Advertisement, Contact, OurTeam, UserProfile, Comment, NewsLetter

# Register your models here.
# admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Advertisement)
admin.site.register(Contact)
admin.site.register(OurTeam)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(NewsLetter)

from django import forms


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget = TinyMCE())

    class Meta:
        model = Post
        fields ="__all__"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
