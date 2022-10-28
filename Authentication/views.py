from django.shortcuts import render, redirect
from .forms import RegisterUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from Authentication.forms import ContactUsForm
import datetime

today = datetime.date.today()
year = today.year


def register_user_view(request):

    form = RegisterUserForm()
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            # user = form.cleaned_data.get("username")
            return redirect("Authentication:login_user")

    context = {"form": form}
    return render(request, "Authentication/register_user.html", context)


def login_user_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(f"/summary/{year}/")
        else:
            messages.info(request, "Username OR password is incorrect")

    form = AuthenticationForm()
    return render(request, "Authentication/login.html", {"form": form})


def logout_user_view(request):
    logout(request)
    return redirect("Authentication:login_user")


def contact_us_view(request):
    form = ContactUsForm()
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            # name = form.cleaned_data.get("name")
            return redirect("Authentication:login_user")
    context = {"contact_form": form}
    return render(request, "Authentication/contact_us.html", context)
