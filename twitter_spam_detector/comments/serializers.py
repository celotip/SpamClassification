from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'author_username',
            'content', 'is_spam', 'spam_reasons', 'created_at'
        ]
        read_only_fields = ['author', 'author_username', 'is_spam', 'spam_reasons', 'created_at']
