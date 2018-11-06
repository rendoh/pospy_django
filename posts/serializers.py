from rest_framework import serializers
from .models import Post, PostImage
from users.serializers import UserSerializer

class PostImageSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    class Meta:
        model = PostImage
        fields = ('image', 'post', 'id')

    def validate_post(self, post):
        user = None
        request = self.context.get('request')
        if (request and hasattr(request, 'user')):
            user = request.user
            if post.user.id == user.id:
                return post
        raise serializers.ValidationError('画像の投稿権限のない記事です')

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = PostImageSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'user', 'created_at', 'images')
