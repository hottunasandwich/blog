from django.shortcuts import render, reverse, redirect
from django.views import generic
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


def get_category_list():
    cat_dict = {}
    categories = Category.objects.all()
    for category in categories:
        if category.parent:
            cat_dict[category.parent.name] += [category.name]
        else:
            cat_dict[category.name] = []

    return cat_dict

class PostsView(generic.ListView):
    template_name = 'blog/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_category_list()
        context['tags'] = Tag.objects.all()
        return context

class PostView(generic.DetailView):
    template_name = 'blog/blog.html'
    model = Post

class PostUpdateView(SuccessMessageMixin, generic.UpdateView):
    template_name = 'blog/edit.html'
    model = Post
    fields = ['title', 'text', 'img', 'tag', 'category']
    success_message = "'%(title)s' was updated successfully"

class PostDeleteView(PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    permission_required = ['delete_post']
    model = Post
    success_url = '/'
    success_message = "'%(title)s' was updated successfully"


@login_required
def post_create_view(request):
    if request.method == 'POST':
        create_form = PostModelForm(request.POST, request.FILES)

        if create_form.is_valid():
            post = create_form.save(commit=False)
            post.author = User.objects.get(username=request.user)
            post.create_date = timezone.now()

            post.save()
            create_form.save_m2m()

            messages.success(request, f'Created Post {post.title}')

            return redirect(reverse('blog:post', kwargs={'pk': post.pk}))

    create_form = PostModelForm()
    return render(request, 'blog/create.html', {'form': create_form})

class TagView(PostsView):
    def setup(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(tag=self.pk)

class CategroyView(TagView):
    def get_queryset(self):
        return Post.objects.filter(Q(category__name=self.pk) | Q(category__parent__name=self.pk))