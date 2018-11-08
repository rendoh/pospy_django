from rest_framework import serializers
from rest_framework.authtoken.models import Token

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

class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Token
        fields = ('key', 'user',)
