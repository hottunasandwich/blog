from django.contrib import admin
from .models import *

class TagAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'create_date', 'approved', 'disabled']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'tag', 'create_date', 'approved', 'disabled']


admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)