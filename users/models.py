from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class UserManager(BaseUserManager):
    """ユーザーマネージャー"""

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        メールアドレスでの登録を必須にする
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=30,
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        null=False,
        blank=False,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

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
