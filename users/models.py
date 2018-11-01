from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    avatar = ProcessedImageField(
        upload_to='avatars/%y/%m/%d',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        blank=True,
        null=True,
        processors=[ResizeToFill(256, 256)],
        format='JPEG'
    )
