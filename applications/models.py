import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.models import User
from users.user_manager import CustomUserManager


class Application(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, related_name="applications", on_delete=models.CASCADE)
    title = models.CharField(max_length=524)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
