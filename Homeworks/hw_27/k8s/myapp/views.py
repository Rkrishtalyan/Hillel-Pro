from django.shortcuts import render
from .models import Entry


def home(request):
    """
    Render the home page with a list of recent entries.

    The home view fetches the latest five entries from the Entry model
    and passes them to the 'home.html' template for rendering.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: The HTTP response with the rendered home page.
    :rtype: HttpResponse
    """
    entries = Entry.objects.all()[:5]
    return render(request, 'myapp/home.html', {'entries': entries})
