# Generated by Django 2.1.2 on 2018-11-05 06:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20181101_0422'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='avatars', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])])),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
        migrations.AddField(
            model_name='useravatar',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='avatar', to=settings.AUTH_USER_MODEL),
        ),
    ]