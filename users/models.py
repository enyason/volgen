import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.user_manager import CustomUserManager


# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="username")
    email = models.EmailField(max_length=300, unique=True, verbose_name="Email address")
    is_email_verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
