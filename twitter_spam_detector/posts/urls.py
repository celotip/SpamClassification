from django.urls import path
from .views import FeedAPIView, CreatePostAPIView, ReportPostAPIView, DeletePostAPIView

urlpatterns = [
    path('api/feed/', FeedAPIView.as_view(), name='api_feed'),
    path('api/create/', CreatePostAPIView.as_view(), name='api_create_post'),
    path('api/report/<int:post_id>/', ReportPostAPIView.as_view(), name='api_report_post'),
    path('api/delete/<int:post_id>/', DeletePostAPIView.as_view(), name='api_delete_post'),
]
