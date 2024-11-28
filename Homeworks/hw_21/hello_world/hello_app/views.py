# ---- Views for Hello App ----

from django.http import JsonResponse
from django.shortcuts import render

from .models import UserProfile


def home(request):
    """
    Render the home page of the application.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: A rendered HTML response for the home page.
    :rtype: HttpResponse
    """
    return render(request, 'hello_app/home.html')


def get_user_profiles(request):
    """
    Fetch and return user profile data in JSON format.

    This view retrieves all user profiles from the database and returns
    a JSON response containing their first and last names.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: A JSON response containing user profiles.
    :rtype: JsonResponse
    """
    user_profiles = list(UserProfile.objects.values('first_name', 'last_name'))
    return JsonResponse({'user_profiles': user_profiles})
