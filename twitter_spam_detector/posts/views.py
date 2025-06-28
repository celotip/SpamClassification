from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from spam_detection.service import SpamDetector


spam_detector = SpamDetector()

def feed(request):
    return render(request, "feed.html")

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        is_spam, reasons = spam_detector.predict(content)
        post = Post.objects.create(
            author=request.user,
            content=content,
            is_spam=is_spam,
            spam_reasons=reasons
        )
        return redirect('feed')
    return render(request, 'create_post.html')

@login_required
def report_post(request, post_id):
    post = Post.objects.get(id=post_id)
    request.user.reported_posts.add(post)
    return redirect('feed')

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id, author=request.user)
    post.delete()
    return redirect('feed')