from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    followers = models.ManyToManyField('self', related_name = 'followees')

    def __str__(self):
        return f"{self.username}"
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": [{"id": u.id, "username": u.username} for u in self.followers.all()],
            "followees": [{"id": u.id, "username": u.username}  for u in self.followees.all()]
        }