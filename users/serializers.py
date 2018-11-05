from rest_framework import serializers
from .models import User, UserAvatar

class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAvatar
        fields = ('image',)

class UserSerializer(serializers.ModelSerializer):
    avatar = UserAvatarSerializer(read_only=True,)
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')
