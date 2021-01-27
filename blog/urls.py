from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('<int:pk>', views.BlogView.as_view(), name='blog')
]