from django import forms
from django.utils import timezone
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'img', 'tag', 'category']

class CommentForm(forms.Form):
    text = forms.CharField(label='Leave a comment', max_length=500)