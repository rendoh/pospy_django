from django.contrib.admin import site
from .models import Post, Relationship

site.register(Post)
site.register(Relationship)
