from django.shortcuts import render
from django.views import generic

# Create your views here.
def BlogView(generic.DetailView):
    template_name = 'blog/blog.html'
    model = Blog