from rest_framework import routers
from .views import UserViewSet, UserAvatarView
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^users/avatar/$', UserAvatarView.as_view()),
]
