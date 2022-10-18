from django.shortcuts import render, redirect
from .forms import RegisterUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def register_user_view(request):
    if request.user.is_authenticated:
        return redirect("summary")
    else:
        form = RegisterUserForm()
        if request.method == "POST":
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, "Account was created for " + user)

                return redirect("Authentication:login_user")

        context = {"form": form}
        return render(request, "Authentication/register_user.html", context)


def login_user_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Log in Successful")
                return redirect("properties:list")
            else:
                messages.info(request, "Username OR password is incorrect")

    form = AuthenticationForm()
    return render(request, "Authentication/login.html", {"form": form})


def logout_user_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("Authentication:login_user")
