from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ums.forms import LoginForm, RegistrationForm, ProfileEditForm, CustomPasswordChangeForm
from ums.models import UserProfile
from utils.email import send_email


def login_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('post_list')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'ums/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have successfully logged out.')
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')

            # Send welcome email
            user_profile = user.userprofile
            if user_profile.email:
                send_email(
                    subject='Welcome to Our Blog!',
                    template_name='emails/registration_email.html',
                    context={'username': user.username},
                    recipient_list=[user_profile.email],
                )

            return redirect('post_list')
    else:
        form = RegistrationForm()
    return render(request, 'ums/register.html', {'form': form})


@login_required
def profile_view(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    return render(request, 'ums/profile.html', {'profile_user': user_profile})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile_view', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user.userprofile)
    return render(request, 'ums/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated.')

            # Send email notification
            user_profile = user.userprofile
            if user_profile.email:
                send_email(
                    subject='Password Changed Successfully',
                    template_name='emails/password_change_email.html',
                    context={'username': user.username},
                    recipient_list=[user_profile.email],
                )

            return redirect('profile_view', username=request.user.username)
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'ums/change_password.html', {'form': form})
