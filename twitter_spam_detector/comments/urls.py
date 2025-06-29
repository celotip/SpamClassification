from django.urls import path
from . import views

urlpatterns = [
    path('post/<int:post_id>/comment/', views.create_comment, name='create_comment'),
    path('comment/<int:comment_id>/report/', views.report_spam, name='report_comment'),
]