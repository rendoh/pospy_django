from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer, UserAvatarSerializer
from rest_framework import mixins, generics
from rest_framework.parsers import FormParser, MultiPartParser

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

class UserAvatarView(mixins.CreateModelMixin, generics.GenericAPIView):

    parser_classes = (FormParser, MultiPartParser,)
    serializer_class = UserAvatarSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # OneToOneのリレーションなので、すでにアバターが存在していたら削除
        if hasattr(self.request.user, 'avatar'):
            self.request.user.avatar.delete()
        serializer.save(user=self.request.user)
