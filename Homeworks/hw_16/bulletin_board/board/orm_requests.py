"""
Module for testing and demonstrating ORM queries in the board app.

This module contains functions to retrieve and manipulate data related to ads,
categories, comments, and users using Django's ORM. Each function serves as a
demonstration of ORM capabilities, with a focus on filtering, aggregating, and
retrieving related objects.

Functions:
    - get_last_month_ads: Retrieve ads created within the last 30 days.
    - get_active_ads_in_category: Retrieve active ads in a specified category.
    - count_comments_for_ad: Count comments for each ad and display the results.
    - get_user_comments: Retrieve ads posted by a specific user.
"""

# ---- Imports ----
from datetime import timedelta
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Ad, Category, UserProfile


# ---- Retrieve Ads from the Last Month ----
def get_last_month_ads():
    """
    Retrieve ads created in the last month.

    :return: QuerySet of ads created in the last 30 days.
    :rtype: QuerySet
    """
    last_month = timezone.now() - timedelta(days=30)
    recent_ads = Ad.objects.filter(created_at__gte=last_month)

    for one_ad in recent_ads:
        print(f"Ad Title: {one_ad.title}, Created At: {one_ad.created_at}")

    return recent_ads


# ---- Get Active Ads in a Specific Category ----
def get_active_ads_in_category(category_name):
    """
    Retrieve active ads in a specified category.

    :param category_name: The name of the category to filter ads.
    :type category_name: str
    :return: QuerySet of active ads in the specified category.
    :rtype: QuerySet
    """
    category = Category.objects.get(name=category_name)
    active_ads_in_category = Ad.objects.filter(is_active=True, category=category)

    for ad in active_ads_in_category:
        print(f"Ad Title: {ad.title}, Category: {category.name}")

    return active_ads_in_category


# ---- Count Comments for Each Ad ----
def count_comments_for_ad():
    """
    Count the number of comments for each ad and print the results.
    """
    ads_with_comment_counts = Ad.objects.annotate(comment_count=Count('comments'))

    for ad in ads_with_comment_counts:
        print(f"Ad Title: {ad.title}, Number of Comments: {ad.comment_count}")


# ---- Retrieve User's Ads ----
def get_user_comments(username):
    """
    Retrieve ads posted by a specific user.

    :param username: The username of the user whose ads are retrieved.
    :type username: str
    :return: QuerySet of ads posted by the user.
    :rtype: QuerySet
    """
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    user_ads = Ad.objects.filter(user=user_profile)

    for ad in user_ads:
        print(f"Ad Title: {ad.title}, Posted by: {ad.user}")

    return user_ads
