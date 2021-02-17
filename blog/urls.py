from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('<int:pk>/post', views.post_view, name='post'),
    path('create/', views.post_create_view, name='create'),
    path('<int:pk>/tag', views.TagView.as_view(), name='tag'),
    path('category/<str:pk>', views.CategroyView.as_view(), name='category'),
    path('<int:pk>/edit', views.PostUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete', views.PostDeleteView.as_view(), name='delete'),
    path('notapproved', views.NotApprovedPostsView.as_view(), name='notapproved'),
    path('<int:pk>/post/actions', views.approve_post, name='approvepost'),
]