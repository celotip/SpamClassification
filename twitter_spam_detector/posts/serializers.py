from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'content', 'is_spam', 'spam_reasons', 'created_at']
        read_only_fields = ['author', 'is_spam', 'spam_reasons', 'created_at']
