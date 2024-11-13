"""
View functions for the board app.

This module provides view functions for displaying a list of ads and the
details of a specific ad along with its comments.

Functions:
    - ad_list: Display a list of active ads.
    - ad_detail: Display details and comments for a specific ad by ID.
    - category_list: Display a list of categories.
    - category_detail: Display ads for a specific category by ID.
    - user_profile: Display a user's profile and their ads.
"""

# ---- Imports ----
from django.shortcuts import render, get_object_or_404
from .models import Ad, Category, Comment, UserProfile

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


def category_list(request):
    """
    Display a list of categories.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered HTML page with the list of categories.
    :rtype: HttpResponse
    """
    categories = Category.objects.all()
    return render(request, 'board/category_list.html', {'categories': categories})


def category_detail(request, category_id):
    """
    Display ads for a specific category.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param category_id: The primary key of the category to display ads for.
    :type category_id: int
    :return: Rendered HTML page with the category details and associated ads.
    :rtype: HttpResponse
    """
    category = get_object_or_404(Category, pk=category_id)
    ads = category.ad_set.filter(is_active=True)
    return render(request, 'board/category_detail.html', {'category': category, 'ads': ads})


def user_profile(request, user_id):
    """
    Display a user's profile and their active ads.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param user_id: The primary key of the user profile to display.
    :type user_id: int
    :return: Rendered HTML page with user profile details and ads.
    :rtype: HttpResponse
    """
    profile = get_object_or_404(UserProfile, pk=user_id)
    ads = Ad.objects.filter(user=profile, is_active=True)
    return render(request, 'board/user_profile.html', {'user_profile': profile, 'ads': ads})
