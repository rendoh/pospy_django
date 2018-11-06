from rest_framework import routers
from .views import PostViewSet, PostImageView
from django.urls import path

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('posts/images/', PostImageView.as_view())
]
