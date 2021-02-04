from django.shortcuts import render, redirect, reverse
from .forms import SignUpForm
from django.views import generic
from django.shortcuts import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = '/users/login'
    template_name = 'users/signup.html'

def login_view(request):
    username = password = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('blog:post', kwargs={'pk': '1'}))

    return render(request, 'users/login.html')

def logout_view(request):
    if request.user and request.method == 'GET':
        logout(request)
        return redirect(reverse('blog:posts'))