from django.urls import path
from . import views

urlpatterns = [
    path('post/<int:post_id>/comment/', views.create_comment, name='create_comment'),
]