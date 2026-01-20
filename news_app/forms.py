from news_app.models import Contact, Comment, NewsLetter
from django import forms

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = "__all__"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)


class NewsLetterForm(forms.ModelForm):
    class Meta:
        model =NewsLetter
        fields = "__all__"