from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Post
from .serializers import PostSerializer
from spam_detection.service import Spam
from django.shortcuts import get_object_or_404

spam = Spam.worker()


class FeedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response({
            'posts': serializer.data,
        })
        

class CreatePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Content is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            is_spam, reasons = spam.predict(content)
            post = Post.objects.create(
                author=request.user,
                content=content,
                is_spam=is_spam,
                spam_reasons=reasons
            )
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportPostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        request.user.reported_comments.add(post)
        return Response({'message': 'Post reported.'})


class DeletePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, author=request.user)
        post.delete()
        return Response({'message': 'Post deleted.'}, status=status.HTTP_204_NO_CONTENT)
