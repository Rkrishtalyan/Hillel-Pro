from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, UserProfileForm, CustomPasswordChangeForm
from .models import UserProfile
from django.contrib.auth.models import User


# ---- User Authentication Views ----
def login_view(request):
    """
    Handle user login requests.

    Redirects authenticated users to their profile.
    On POST, attempts to authenticate and log in the user.
    """
    if request.user.is_authenticated:
        return redirect('profile_view', username=request.user.username)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('profile_view', username=user.username)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'ums/login.html', {'form': form})


def logout_view(request):
    """
    Handle user logout requests.

    Logs out the user and redirects to the login page.
    """
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have successfully logged out.')
    return redirect('login')


def register_view(request):
    """
    Handle user registration requests.

    On POST, creates a new user and logs them in.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('profile_view', username=user.username)
    else:
        form = RegistrationForm()
    return render(request, 'ums/register.html', {'form': form})


# ---- Profile Management Views ----
@login_required
def edit_profile_view(request):
    """
    Handle profile editing requests for authenticated users.

    On POST, updates the user's profile with submitted data.
    """
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.userprofile
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated.')
            return redirect('profile_view', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'ums/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    """
    Handle password change requests for authenticated users.

    On POST, validates and updates the user's password.
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated.')
            return redirect('profile_view', username=request.user.username)
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'ums/change_password.html', {'form': form})


@login_required
def profile_view(request, username):
    """
    Display the profile page for a specified user.

    :param username: The username of the profile to display.
    """
    profile_user = get_object_or_404(User, username=username)
    return render(request, 'ums/profile.html', {'profile_user': profile_user})
