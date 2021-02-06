from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission

class CategoryAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'create_date', 'approved', 'disabled']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'tag', 'create_date', 'approved', 'disabled']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)