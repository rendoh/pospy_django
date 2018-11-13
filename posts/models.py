import urllib.parse
from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Q
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill
from users.models import User
from imagekit.cachefiles.backends import CacheFileState

class Post(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    visual = models.OneToOneField(
        'PostImage',
        on_delete=models.CASCADE,
        related_name='_post',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)

class PostImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images',
        null=True,
        blank=True,
        default=None
    )
    created_at = models.DateTimeField(auto_now_add=True)
    image = ProcessedImageField(
        upload_to='posts',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        processors=[ResizeToFit(980, upscale=False)],
        format='JPEG'
    )
    thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(640, 360)],
        format='JPEG'
    )

@receiver(post_save, sender=Post)
def delete_unused_images(sender, instance, **kwargs): #pylint: disable=unused-argument
    """
    不要なメディアファイルを削除する
    """
    post_id = instance.id
    body = instance.body

    # この投稿の中で使用されていることを期待される画像と
    # 使用されている記事が指定されていない画像を取得
    used_post_images = PostImage.objects.filter(
        Q(post=post_id) | Q(post=None)
    )
    for used_post_image in used_post_images:
        # * 本文中で使われているかどうか
        # * ビジュアルに指定されているかどうか
        # により、使用先記事を指定 or 空にする

        url = urllib.parse.quote(str(used_post_image.image))
        if url in body or instance.visual == used_post_image:
            used_post_image.post = instance
        else:
            used_post_image.post = None
        used_post_image.save()

    # 使用されている記事が指定されていない画像を削除
    instance.user.delete_unused_post_images()

@receiver(post_delete, sender=PostImage)
def delete_image_files(sender, instance, **kwargs):
#pylint: disable=unused-argument
    """
    キャッシュをクリアする
      不要となった画像のサムネイル等のリサイズされた画像を削除
    """
    image = instance.thumbnail
    image.storage.delete(image)
    image.cachefile_backend.set_state(image, CacheFileState.DOES_NOT_EXIST)
