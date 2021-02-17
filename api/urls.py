from rest_framework import routers
from api import views
from django.urls import path


router = routers.SimpleRouter()
router.register('comment/like', views.CommentLikeViewSet)
router.register('post/like', views.PostLikeViewSet)

app_name = 'api'
urlpatterns = router.urls + [
    path('post/notapproved', views.NotApprovedView.as_view(), name='notapproved')
]