from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
from .models import User
from .tfa import generate_verification_code, send_tfa_email
from django.core.cache import cache
import requests
import os

# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            verification_code = generate_verification_code()
            email = form.cleaned_data["email"]
            cache.set(email, verification_code, timeout=300)
            send_tfa_email(email, verification_code)
            return render(request, 'authentication/verify_tfa.html', {'email': user.email})
        else:
            messages.error(request, form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

def verify_tfa_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        secret_key = request.POST.get('verification_code')
        # Verify the secret key entered by the user against the secret key generated during registration
        try:
            user = User.objects.get(email=email, secret_key=secret_key)
        except User.DoesNotExist:
            messages.error(request, 'Invalid secret key')
            return redirect('register')
        # Create the user account and log them in
        user.save()
        login(request, user)
        return redirect('index')
    else:
        email = request.GET.get('email')
        if email is None:
            return redirect('register')
        return render(request, 'authentication/verify_2fa.html', {'email': email})

def login_view(request):
    """
    Handle a user logging in to MotorPlus.
    
    If the request method is "POST", the function checks the provided username and password against the 
    database to authenticate the user. If the user is authenticated, the user is logged in and redirected 
    to the index page. If the user is not authenticated, an error message is displayed and the login form 
    is shown again. If the request method is not "POST", the login form is displayed.
    
    Returns:
        If the request method is "POST" and the user is not authenticated:
            The login form, with the error message passed in as context.
        If the request method is not "POST":
            The login form.
        Otherwise:
            A redirect to the index page.
    """
    
    # If the user has submitted the form
    if request.method == "POST":
        # Validate the form data
        email = request.POST.get('inputEmail')
        password = request.POST.get('inputPassword')
        user = authenticate(request, email=email, password=password)
        
        # If the user is authenticated
        if user is not None:
            login(request, user)
            return redirect('index')
        
        # If the user is not authenticated
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'authentication/login.html')
    
    # If the user has not submitted the form
    else:
        # Display the login form
        return render(request, 'authentication/login.html')
    
    
def logout_view(request):
    logout(request)
    return redirect('login')