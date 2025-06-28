from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True)

    class Meta:
        # Add this to prevent reverse accessor clashes
        db_table = 'custom_user'