# ---- Import Statements ----
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ums.forms import LoginForm, RegistrationForm, ProfileEditForm, CustomPasswordChangeForm
from ums.models import UserProfile
from utils.email import send_email


# ---- View Functions ----

def login_view(request):
    """
    Handle user login functionality.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered template for the login page or a redirect upon successful login.
    :rtype: HttpResponse
    """
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
    """
    Handle user logout functionality.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Redirect to the login page after logout.
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have successfully logged out.')
    return redirect('login')


def register_view(request):
    """
    Handle user registration functionality.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered template for the registration page or a redirect upon successful registration.
    :rtype: HttpResponse
    """
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
    """
    Display the profile of a user.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param username: The username of the profile to display.
    :type username: str
    :return: Rendered template for the user profile page.
    :rtype: HttpResponse
    """
    user_profile = get_object_or_404(UserProfile, user__username=username)
    return render(request, 'ums/profile.html', {'profile_user': user_profile})


@login_required
def edit_profile(request):
    """
    Allow the logged-in user to edit their profile.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered template for editing the profile or a redirect upon successful update.
    :rtype: HttpResponse
    """
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
    """
    Allow the logged-in user to change their password.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered template for changing the password or a redirect upon successful update.
    :rtype: HttpResponse
    """
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
