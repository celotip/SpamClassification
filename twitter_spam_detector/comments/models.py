from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post  # Minimal dependency

User = get_user_model()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_spam = models.BooleanField(default=False)
    spam_reasons = models.JSONField(default=list)

    def __str__(self):
        return f"Comment by {self.author.username}"