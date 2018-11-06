from django.db import models
from users.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.core.validators import FileExtensionValidator

class Post(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

class PostImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    image = ProcessedImageField(
        upload_to='posts',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        processors=[ResizeToFit(980, upscale=False)],
        format='JPEG'
    )
