from django import template
from blog.models import CommentLike, PostLike
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def like_counter(value, like):
    counter = 0
    for comment_like in value:
        if comment_like.like == like:
            counter += 1
    
    return counter

@register.filter
def liked_this_post(value, user):
    user = User.objects.get(username=user)
    if user:
        post_like = PostLike.objects.get(post=value, user=user)
        if post_like:
            return post_like.like

    return None

@register.filter
def comment_liked(value, user):
    user = User.objects.get(username=user)
    if user:
        comment_like = CommentLike.objects.get(comment=value, user=user)
        if comment_like:
            return comment_like.like

    return None