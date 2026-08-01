from django.shortcuts import render


def login_view(request):
    return render(request, "accounts/login.html")


def register_view(request):
    return render(request, "accounts/register.html")


def profile(request):
    return render(request, "accounts/profile.html")


def my_bookings(request):
    return render(request, "accounts/my_bookings.html")


def logout_view(request):
    pass