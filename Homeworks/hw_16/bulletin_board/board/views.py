"""
View functions for the board app.

This module provides view functions for displaying a list of ads and the
details of a specific ad along with its comments.

Functions:
    - ad_list: Display a list of active ads.
    - ad_detail: Display details and comments for a specific ad by ID.
"""

# ---- Imports ----
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Ad, Category, Comment

# ---- View Functions ----

def ad_list(request):
    """
    Display a list of active ads.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered HTML page with the list of active ads.
    :rtype: HttpResponse
    """
    ads = Ad.objects.filter(is_active=True)
    return render(request, 'board/ad_list.html', {'ads': ads})


def ad_detail(request, ad_id):
    """
    Display details for a specific ad and its associated comments.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param ad_id: The primary key of the ad to display.
    :type ad_id: int
    :return: Rendered HTML page with ad details and comments.
    :rtype: HttpResponse
    """
    ad = get_object_or_404(Ad, pk=ad_id)
    comments = ad.comments.all()
    return render(request, 'board/ad_detail.html', {'ad': ad, 'comments': comments})
