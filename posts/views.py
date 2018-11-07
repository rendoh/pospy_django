from rest_framework import viewsets, permissions
from rest_framework import mixins, generics
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Post
from .serializers import PostSerializer, PostImageSerializer
from .permissions import IsOwnerOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostImageView(mixins.CreateModelMixin, generics.GenericAPIView):

    parser_classes = (FormParser, MultiPartParser,)
    serializer_class = PostImageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
