from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import generic
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .forms import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users.management.commands.creategroups import Command as Perms
from django.http import HttpResponse


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
        if self.request.user.has_perms(Perms.editor_perms):
            return Post.objects.all()

        return Post.objects.filter(disabled=False, approved=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_category_list()
        context['tags'] = Tag.objects.all()
        return context

def post_view(request, pk):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)

    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST' and user.has_perm('blog.add_comment'):
        new_comment_form = CommentForm(request.POST)

        if new_comment_form.is_valid():
            text = new_comment_form.cleaned_data['text']

            Comment.objects.create(text=text, author=user, post=post)

            messages.success(request, 'Comment added')

    new_comment_form = CommentForm()

    return render(request, 'blog/blog.html', {'post': post, 'form': new_comment_form})

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
        if self.request.user.has_perms(Perms.editor_perms):
            return Post.objects.filter(tag=self.pk)
        return Post.objects.filter(tag=self.pk, approved=True, disabled=False)

class CategroyView(TagView):
    def get_queryset(self):
        if self.request.user.has_perms(Perms.editor_perms):
            return Post.objects.filter(Q(category__name=self.pk) | Q(category__parent__name=self.pk))
        return Post.objects.filter(Q(category__name=self.pk) | Q(category__parent__name=self.pk), approved=True, disabled=False)

@permission_required('blog.change_post')
def approve_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        if request.POST['action'] == 'approve':
            post.approved = True
            messages.success(request, f'Approved "{post}"')
            post.save()

            return redirect(reverse('blog:notapproved'))

        elif request.POST['action'] == 'enable':
            post.disabled = not post.disabled
            messages.success(request, f'{"Disabled" if post.disabled else "Enabled" } "{post}"')

        post.save()

        return HttpResponse('ok')
class NotApprovedPostsView(PostsView):
    def get_queryset(self):
        return Post.objects.filter(approved=False)