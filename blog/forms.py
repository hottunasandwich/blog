from django import forms
from django.utils import timezone
from .models import Post

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'img']