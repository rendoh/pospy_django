from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    original_avatar = models.ImageField(
        upload_to='avatars/%y/%m/%d',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )
    avatar = ImageSpecField(
        source='original_avatar',
        processors=[ResizeToFill(256, 256)],
        format='JPEG',
    )
