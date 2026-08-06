# accounts_app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth import authenticate, login ,logout
from home_app.views import home

# accounts_app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
import re
from .models import CustomUser


def register(request):
    """
    Production-level user registration view with comprehensive validation.
    """
    if request.method == "POST":
        # Get and sanitize input
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        errors = []

        if not username:
            errors.append("Username is required.")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters long.")
        elif len(username) > 150:
            errors.append("Username cannot exceed 150 characters.")
        elif not re.match(r'^[\w.@+-]+\Z', username):
            errors.append("Username contains invalid characters. Use letters, digits, and @/./+/-/_ only.")
        
        if not email:
            errors.append("Email address is required.")
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append("Please enter a valid email address.")
        
        if not confirm_password:
            errors.append("Please type confirm password.")
        elif password != confirm_password:
            errors.append("Passwords do not match.")
        
        if CustomUser.objects.filter(username__iexact=username).exists():
            messages.error(request, "This username is already taken. Please choose another.")
            return redirect("register")
        
        # Check if email exists
        if CustomUser.objects.filter(email__iexact=email).exists():
            messages.error(request, "An account with this email already exists. Please use a different email or login.")
            return redirect("register")
        
        try:
            # Django's built-in password validators
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect("register")

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                address=address,
                phone_number=phone,
                is_active=True 
            )
            user.save()  
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
            
        except IntegrityError:
            messages.error(request, "An error occurred while creating your account. Please try again.")
            return redirect("register")
        except Exception as e:
            messages.error(request, "An unexpected error occurred. Please try again later.")
            return redirect("register")
    
    return render(request, 'register.html')

def signin(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        rememberme=request.POST.get("rememberme")

        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request,"username not found")
            return redirect("login")
            
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            if rememberme:
                request.session.set_expiry(12) #12seconds
            else:
                request.session.set_expiry(0)
            messages.success(request,"login succesfully")
            return redirect('home')
        else:
            messages.error(request,"paassword doesnt match")
            return redirect('login')    
    return render(request,'login.html')

def signout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')