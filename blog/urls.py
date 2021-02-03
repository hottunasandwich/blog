from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('<int:pk>', views.PostView.as_view(), name='post'),
    path('create/', views.post_create_view, name='create')
]