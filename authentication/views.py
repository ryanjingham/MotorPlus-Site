from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password
from django.core.exceptions import MultipleObjectsReturned
from .forms import LoginForm, UserRegistrationForm
from .models import User
from .tfa import generate_verification_code, send_tfa_email
from django.core.cache import cache
import requests
import os
import secrets


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # if User.objects.filter(email=email).exists():
            #     messages.error(request, "Email has already been used.")
            #     return redirect("login")

            # Make an API request to generate the API key
            api_key_response = requests.post(
                "http://127.0.0.1:5000/register",
                data={"username": form.cleaned_data["username"], "email": email},
            )

            if api_key_response.status_code == 200:
                api_key = api_key_response.json()["api_key"]
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=email,
                    password=form.cleaned_data["password1"],
                    API_KEY=api_key,
                )
                user.save()

                verification_code = generate_verification_code()
                cache.set(email, verification_code, timeout=300)
                cache.set(
                    form.cleaned_data["username"],
                    form.cleaned_data["password1"],
                    timeout=300,
                )
                send_tfa_email(email, verification_code)

                return redirect(
                    "verify_tfa", email=email, username=form.cleaned_data["username"]
                )

            else:
                messages.error(request, "Failed to generate API key.")
                return redirect("register")

        else:
            messages.error(request, form.errors)

    else:
        form = UserRegistrationForm()

    return render(request, "authentication/register.html", {"form": form})


def verify_tfa_view(request, email, username):
    if request.method == "POST":
        print("post")
        verification_code = request.POST.get("verification_code")
        cached_verification_code = cache.get(email)
        if cached_verification_code == verification_code:
            # Verification successful, create user and log in
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                password = cache.get(username)
                hashed_password = make_password(password)
                user = User(email=email, username=username, password=hashed_password)
                user.save()
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid verification code")
            return redirect(request.path_info)
    else:
        print("get")
        password = cache.get(username)
        if email is None or username is None or password is None:
            print("email or username or password none")
            return redirect("register")
        return render(
            request,
            "authentication/verify_tfa.html",
            {"email": email, "username": username, "password": password},
        )


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("inputEmail")
        password = request.POST.get("inputPassword")
        print(f"email: {email}   password: {password}")

        try:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                verification_code = generate_verification_code()
                cache.set(email, verification_code, timeout=300)
                send_tfa_email(email, verification_code)
                return redirect("verify_tfa", email=email, username=user.username)

            else:
                messages.error(request, "Invalid username or password.")
                return render(request, "authentication/login.html")

        except MultipleObjectsReturned:
            messages.error(
                request,
                "Multiple users found with the same email. Please contact support.",
            )
            return render(request, "authentication/login.html")

    else:
        return render(request, "authentication/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
