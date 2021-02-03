from django.shortcuts import render, reverse, redirect
from django.views import generic
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.
class PostsView(generic.ListView):
    
    template_name = 'blog/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()


class PostView(generic.DetailView):
    template_name = 'blog/blog.html'
    model = Post

@login_required
def post_create_view(request):
    if request.method == 'POST':
        print(request.POST, request.FILES)
        create_form = PostModelForm(request.POST, request.FILES)

        if create_form.is_valid():
            post = create_form.save(commit=False)
            post.author = User.objects.get(username=request.user)
            post.create_date = timezone.now()

            post.save()
            create_form.save_m2m()

            return redirect(reverse('blog:post', kwargs={'pk': post.pk}))

        else:
            print(create_form.cleaned_data)

    create_form = PostModelForm()
    return render(request, 'blog/create.html', {'form': create_form})