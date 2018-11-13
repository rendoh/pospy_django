# Generated by Django 2.1.2 on 2018-11-13 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20181107_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visual',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='_post', to='posts.PostImage'),
        ),
    ]
