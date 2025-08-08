from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponse



otp_storage = {}  # Temporary OTP store

def home(request):
    return render(request, 'events/home.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return HttpResponse("Passwords do not match.")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already taken.")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)
        return redirect('dashboard')
    
    return render(request, 'events/signup.html')

def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST['otp']
        email = request.session['email']
        if otp_storage.get(email) == user_otp:
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            del otp_storage[email]
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP")
    return render(request, 'events/verify_otp.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'events/login.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'events/dashboard.html')

def logout_view(request):
    auth.logout(request)
    return redirect('home')
