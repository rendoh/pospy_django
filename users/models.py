from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    def get_followers(self):
        relations = Relationship.objects.filter(owner=self)
        return [relation.follower for relation in relations]

    def get_users_following_me(self):
        relations = Relationship.objects.filter(follower=self)
        return [relation.owner for relation in relations]

    def get_post_images(self):
        from posts.models import PostImage
        post_images = PostImage.objects.filter(user=self)
        return post_images

    def delete_unused_post_images(self):
        """
        Postと紐付いていない画像を削除
        """
        from posts.models import PostImage
        post_images = PostImage.objects.filter(user=self).filter(post=None)
        for post_image in post_images:
            post_image.delete()


class UserAvatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')
    created_at = models.DateTimeField(auto_now_add=True)
    image = ProcessedImageField(
        upload_to='avatars',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        processors=[ResizeToFill(256, 256)],
        format='JPEG'
    )

class Relationship(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owners')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
