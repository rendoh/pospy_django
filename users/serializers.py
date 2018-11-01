from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # avatarはオブジェクトなので、urlのみを抽出する
    avatar = serializers.CharField(source='avatar.url')

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')
