from django.db import models
from users.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_spam = models.BooleanField(default=False)
    spam_reasons = models.JSONField(default=list, blank=True)