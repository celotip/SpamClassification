from django.contrib import admin
from django.urls import path
from posts import views as post_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', post_views.feed, name='feed'),
    path('post/create/', post_views.create_post, name='create_post'),
    path('post/delete/<int:post_id>/', post_views.delete_post, name='delete_post'),
    path('post/report/<int:post_id>/', post_views.report_post, name='report_post'),
    path('user/block/<int:user_id>/', user_views.block_user, name='block_user'),
]