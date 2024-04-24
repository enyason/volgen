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


class Gender(models.TextChoices):
    MALE = 'male'
    FEMALE = 'female'


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, related_name="submissions", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    cover_letter = models.TextField(null=True, blank=True, max_length=1024)
    email = models.EmailField()
    gender = models.CharField(choices=Gender.choices, max_length=24, null=True, blank=True)
    country = models.CharField(max_length=64)
    resume = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
