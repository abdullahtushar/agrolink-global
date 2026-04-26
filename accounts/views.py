"""
Accounts Views — Auth & Profile Management
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to AgroLink Global, {user.first_name}!')
            return redirect('login_redirect')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('login_redirect')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Log out user."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def login_redirect_view(request):
    """Redirect users to their role-based dashboard after login."""
    if request.user.is_farmer:
        return redirect('farmer_dashboard')
    elif request.user.is_exporter:
        return redirect('exporter_dashboard')
    elif request.user.is_admin_user or request.user.is_superuser:
        return redirect('/admin/')
    return redirect('home')


@login_required
def profile_view(request):
    """View and update user profile."""
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
