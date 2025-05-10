from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.filter(username=username).first()
        if user is not None and user.check_password(password):
            auth_login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "insightfulbyte/login.html",
                {"error": "Invalid username or password"},
            )
    else:
        return render(request, "insightfulbyte/login.html")


def logout(request):
    auth_logout(request)
    return redirect("home")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        user.save()
        return redirect("login")
    else:
        return render(request, "insightfulbyte/register.html")


def profile(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_profile":
            username = request.POST.get("username")
            email = request.POST.get("email")

            if (
                username != request.user.username
                and User.objects.filter(username=username).exists()
            ):
                messages.error(
                    request, "Username already taken. Please choose another one."
                )
                return redirect("profile")

            user = request.user
            user.username = username
            user.email = email
            user.save()

            messages.success(request, "Profile updated successfully!")
            return redirect("profile")

        elif action == "change_password":
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not request.user.check_password(current_password):
                messages.error(request, "Current password is incorrect")
                return redirect("profile")

            if new_password != confirm_password:
                messages.error(request, "New passwords do not match")
                return redirect("profile")

            if len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters")
                return redirect("profile")

            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "Password changed successfully!")
            return redirect("login")

    return render(request, "insightfulbyte/profile.html")


def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("password_change_done")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "insightfulbyte/profile.html", {"form": form})
