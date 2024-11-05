from django.shortcuts import render

# ---- View Functions for Each Page ----

def home(request):
    """
    Render the home page.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered home page.
    :rtype: HttpResponse
    """
    return render(request, 'home/home.html')

def about(request):
    """
    Render the about page.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered about page.
    :rtype: HttpResponse
    """
    return render(request, 'home/about.html')

def contact(request):
    """
    Render the contact page.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered contact page.
    :rtype: HttpResponse
    """
    return render(request, 'home/contact.html')

def post_view(request, id):
    """
    Render a post page with a specific post ID.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param id: The ID of the post.
    :type id: int
    :return: Rendered post page with the given ID.
    :rtype: HttpResponse
    """
    context = {'id': id}
    return render(request, 'home/post.html', context)

def profile_view(request, username):
    """
    Render a user profile page with a specific username.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param username: The username of the profile.
    :type username: str
    :return: Rendered profile page with the given username.
    :rtype: HttpResponse
    """
    context = {'username': username}
    return render(request, 'home/profile.html', context)

def event_view(request, year, month, day):
    """
    Render an event page for a specific date.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param year: The year of the event.
    :type year: int
    :param month: The month of the event.
    :type month: int
    :param day: The day of the event.
    :type day: int
    :return: Rendered event page with the specified date.
    :rtype: HttpResponse
    """
    context = {
        'year': year,
        'month': month,
        'day': day
    }
    return render(request, 'home/event.html', context)
