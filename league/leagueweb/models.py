from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    # Add custom fields here if needed
    # For example, you can add a profile picture field:
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
