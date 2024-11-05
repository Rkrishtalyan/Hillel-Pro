from django.http import HttpResponse
from django.shortcuts import render


# ---- View Functions for Main Pages ----

def home(request):
    """
    Render the home page.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered home page response.
    :rtype: HttpResponse
    """
    return render(request, 'home/home.html')


def about(request):
    """
    Return a simple response for the 'About us' page.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: 'About us' page response.
    :rtype: HttpResponse
    """
    return HttpResponse('"About us" page')


def contact(request):
    """
    Return a simple response for the contact page.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Contact page response.
    :rtype: HttpResponse
    """
    return HttpResponse('Contact us!')


# ---- View Functions with URL Parameters ----

def post_view(request, id):
    """
    Display a post based on its ID.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param id: The ID of the post to view.
    :type id: int
    :return: Response with the post number.
    :rtype: HttpResponse
    """
    return HttpResponse(f'You view post number {id}')


def profile_view(request, username):
    """
    Display the profile of a user based on the username.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param username: The username of the profile to view.
    :type username: str
    :return: Response with the profile information.
    :rtype: HttpResponse
    """
    return HttpResponse(f'You view profile of user {username}')


def event_view(request, year, month, day):
    """
    Display an event based on the provided date.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param year: The year of the event.
    :type year: int
    :param month: The month of the event.
    :type month: int
    :param day: The day of the event.
    :type day: int
    :return: Response with the event date.
    :rtype: HttpResponse
    """
    return HttpResponse(f'Event date: {year}-{month}-{day}')
