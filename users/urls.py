from django.urls import include, path
from .views import SignUpView, login_view, logout_view, UserProfileUpdate


app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('<int:pk>/profile/', UserProfileUpdate.as_view(), name='profile')
]