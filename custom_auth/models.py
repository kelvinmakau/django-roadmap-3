# custom_auth/models.py
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    designation = models.CharField(max_length=100)

    # Override built in group to avoid clash with custom gtoup
    custom_groups = models.ManyToManyField(
        Group,
        related_name='custom_users',
        blank=True,
    )

    # Add a related_name to the user_permissions field
    user_permissions = models.ManyToManyField(
        to='auth.Permission',
        related_name='custom_users',
        blank=True,
    )