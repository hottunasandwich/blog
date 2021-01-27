from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    text = models.CharField('Text', max_length=9000)
    img = models.CharField('Image', max_length=100)
    create_date = models.DateField('Date')
    title = models.CharField('Title', max_length=100)
    user_id = models.ForeignKey(User)
    tag_id = models.ForeignKey('Tag')


class Tag(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Tag)

class Comment(models.Model):
    text = models.CharField('Text', max_length=9000)
    create_date = models.DateField('Date')
    user_id = models.ForeignKey(User)
    post_id = models.ForeignKey(Post)
