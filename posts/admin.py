from django.contrib.admin import site
from .models import Post, PostImage

site.register(Post)
site.register(PostImage)
