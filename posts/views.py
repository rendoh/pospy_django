from rest_framework import viewsets, permissions
from rest_framework import mixins, generics
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Post, PostImage
from .serializers import PostSerializer, PostImageSerializer
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q

def delete_unused_images(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        serializer = args[1]
        function(*args, **kwargs)
        body = serializer.data['body']
        post_id = serializer.data['id']
        post = Post.objects.get(pk=post_id)
        used_post_images = PostImage.objects.filter(
            Q(post=post_id) | Q(post=None)
        )
        for used_post_image in used_post_images:
            url = str(used_post_image.image)
            if url in body:
                used_post_image.post = post
            else:
                used_post_image.post = None
            used_post_image.save()
        self.request.user.delete_unused_post_images()
    return wrapper

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @delete_unused_images
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @delete_unused_images
    def perform_update(self, serializer):
        serializer.save()


class PostImageView(mixins.CreateModelMixin, generics.GenericAPIView):

    parser_classes = (FormParser, MultiPartParser,)
    serializer_class = PostImageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
