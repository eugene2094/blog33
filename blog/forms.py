from django import forms
from django.contrib.auth.models import User

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('published_date', 'user','comments')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('post', 'author', 'published_date')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']