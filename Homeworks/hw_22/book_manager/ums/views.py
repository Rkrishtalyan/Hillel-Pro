from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta

from ums.forms import LoginForm


# ---- Login View ----
def login_view(request):
    """
    Handle user login and set session and cookies.

    If the request method is POST and the form is valid:
    - Store the user's name in a cookie (expires in 30 minutes).
    - Store the user's age in the session.
    - Redirect to the greeting view.

    If the request method is GET, display the login form.

    :param request: The HTTP request object.
    :return: Rendered login page or redirect to the greeting page.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            age = form.cleaned_data.get('age')

            response = redirect('greeting')
            expires = timezone.now() + timedelta(minutes=30)
            response.set_cookie('name', name, expires=expires)

            request.session['age'] = age

            return response
    else:
        form = LoginForm()

    return render(request, 'ums/login.html', {'form': form})


# ---- Greeting View ----
def greeting_view(request):
    """
    Display a personalized greeting for the logged-in user.

    If the 'name' cookie and 'age' session variable exist:
    - Render the greeting page and refresh the 'name' cookie expiration.

    If they do not exist:
    - Inform the user about the expired session and redirect to the login page.

    :param request: The HTTP request object.
    :return: Rendered greeting page or redirect to the login page.
    """
    name = request.COOKIES.get('name')
    age = request.session.get('age')

    if name and age:
        response = render(request, 'ums/greeting.html', {'name': name, 'age': age})
        expires = timezone.now() + timedelta(minutes=30)
        response.set_cookie('name', name, expires=expires)
        return response
    else:
        messages.info(request, "Your session has expired. Please log in again.")
        return redirect('login')


# ---- Logout View ----
def logout_view(request):
    """
    Handle user logout by clearing session data and cookies.

    - Deletes the 'name' cookie.
    - Flushes the session data.
    - Redirects the user to the login page.

    :param request: The HTTP request object.
    :return: Redirect to the login page.
    """
    response = redirect('login')
    response.delete_cookie('name')
    request.session.flush()
    return response
