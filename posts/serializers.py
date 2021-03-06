from rest_framework import serializers
from .models import Post, PostImage
from users.serializers import UserSerializer

class PostImageSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(read_only=True)
    class Meta:
        model = PostImage
        fields = ('image', 'id', 'thumbnail')

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'user', 'created_at', 'visual')
