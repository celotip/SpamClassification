from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Post
from .models import Comment
from spam_detection.service import Spam;

spam = Spam.worker()

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        is_spam, reasons = spam.predict(content)
        print('is_spam, reasons', is_spam, reasons) 
        try:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
                is_spam=is_spam,
                spam_reasons=reasons
            )
            print("Comment created:", comment.id)  # Debug
            return redirect('feed')
        except Exception as e:
            print("Error:", str(e))  # Debug
    return redirect('feed')

@login_required
def report_spam(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Add reporting user to reported_by
    comment.reported_by.add(request.user)
    
    # Optional: Auto-mark as spam if enough reports
    if comment.reported_by.count() >= 3:  # Threshold configurable
        comment.is_spam = True
        comment.spam_reasons.append(f"Reported by {comment.reported_by.count()} users")
        comment.save()
    
    return redirect('feed')  # Or your preferred redirect