from django.contrib.auth.decorators import login_required
from users.models import User
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm
from .models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

@login_required
def block_user(request, user_id):
    user_to_block = User.objects.get(id=user_id)
    request.user.blocked_users.add(user_to_block)
    return redirect('feed')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("feed"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "users/login.html")

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('feed')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("feed"))

def profile(request):
    return render(request, 'users/profile.html')