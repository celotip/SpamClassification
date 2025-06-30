from django.urls import path
from .views import CreateCommentAPIView, DeleteCommentAPIView, PostCommentsAPIView, ReportSpamCommentAPIView

urlpatterns = [
    path('posts/<int:post_id>/comments/', PostCommentsAPIView.as_view(), name='api_post_comments'),
    path('posts/<int:post_id>/comments/create/', CreateCommentAPIView.as_view(), name='api_create_comment'),
    path('comments/<int:comment_id>/report/', ReportSpamCommentAPIView.as_view(), name='api_report_comment'),
    path('comments/<int:comment_id>/delete/', DeleteCommentAPIView.as_view(), name='api_comment_delete'),
]