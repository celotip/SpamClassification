from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
from sklearn.model_selection import train_test_split
from .models import Post
from spam_detection.service import Spam;

spam = Spam.worker()

def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    accuracy = Spam.evaluate() 
    return render(request, 'feed.html', {'posts': posts, 'accuracy' : accuracy})  # Pass posts to the template


# Create post & comment section
@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        is_spam, reasons = spam.predict(content)
        try:
            is_spam, reasons = spam.predict(content)
            post = Post.objects.create(
                author=request.user,
                content=content,
                is_spam=is_spam,
                spam_reasons=reasons
            )
            print("Post created:", post.id)  # Debug
            return redirect('feed')
        except Exception as e:
            print("Error:", str(e))  # Debug
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