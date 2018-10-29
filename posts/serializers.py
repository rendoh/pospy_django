from rest_framework import serializers
from .models import Post
from users.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'user', 'created_at',)
