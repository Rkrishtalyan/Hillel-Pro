"""
Context processors for the web_site app.

This module defines custom context processors to inject global data into
templates.
"""

# Task 4

def global_data(request):
    """
    Provide global data for use in templates.

    This context processor injects the site name into the template context.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: A dictionary containing global data.
    :rtype: dict
    """
    return {
        'SITE_NAME': 'Homework 23 - Customization in Django'
    }
