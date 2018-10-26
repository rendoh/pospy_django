from django.db import models
from django.contrib.auth.models import User 

class Post(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_followers(self):
        relations = Relationship.objects.filter(owner=self)
        return [relation.follower for relation in relations]

    def get_users_following_me(self):
        relations = Relationship.objects.filter(follower=self)
        return [relation.owner for relation in relations]

class Relationship(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owners')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
