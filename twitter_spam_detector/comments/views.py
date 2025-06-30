from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from posts.models import Post
from .models import Comment
from .serializers import CommentSerializer  # You'll define this
from spam_detection.service import Spam

spam = Spam.worker()


class PostCommentsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all().order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateCommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        content = request.data.get('content')

        if not content:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

        is_spam, reasons = spam.predict(content)

        if is_spam:
            Spam.retrain_with_reported_data([(content, 1)]) # 1 means spam

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            is_spam=is_spam,
            spam_reasons=reasons
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportSpamCommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        
        comment.reported_by.add(request.user)

        if comment.reported_by.count() >= 3:
            comment.is_spam = True
            Spam.retrain_with_reported_data([(comment.content, 1)])
            comment.spam_reasons.append(f"Reported by {comment.reported_by.count()} users")
            comment.save()
    

        return Response({'message': 'Comment reported successfully.'}, status=status.HTTP_200_OK)

class DeleteCommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, author=request.user)
        comment.delete()
        return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)