from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django.shortcuts import reverse
from django.contrib.postgres.search import SearchVectorField

fs = FileSystemStorage(location='media')

class Post(models.Model):
    text = models.CharField('Text', max_length=9000)
    img = models.ImageField(storage=fs)
    create_date = models.DateField('Date', auto_now_add=True)
    title = models.CharField('Title', max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, null=True, blank=True)
    tag = models.ManyToManyField('Tag')
    disabled = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    search_vector = SearchVectorField(null=True, editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'pk': self.pk})

    def delta_time(self):
        pass

    class Meta:
        ordering = ['-create_date']

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'#{self.name}'

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)

    def clean(self, *args, **kwargs):
        if self.parent:
            if self.parent.pk == self.pk:
                raise ValidationError(_('parent can not be as same as this foreign key'))

        super().clean(*args, **kwargs)

    def full_name(self):
        return f'{str(self.parent) + "/" if self.parent else ""}{self.name}'

    def __str__(self):
        return self.full_name()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Comment(models.Model):
    text = models.CharField('Text', max_length=9000)
    create_date = models.DateField('Date', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    disabled = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class CommentLike(models.Model):
    like = models.BooleanField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class PostLike(models.Model):
    like = models.BooleanField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)