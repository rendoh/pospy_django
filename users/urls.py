from rest_framework import routers
from .views import UserViewSet, UserAvatarView
from django.urls import path

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('users/avatar', UserAvatarView.as_view()),
]
