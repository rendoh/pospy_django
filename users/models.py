from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    pass

class UserAvatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')
    created_at = models.DateTimeField(auto_now_add=True)
    image = ProcessedImageField(
        upload_to='avatars',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        processors=[ResizeToFill(256, 256)],
        format='JPEG'
    )
