"""
URL configuration for the board app.

This module defines URL patterns for the board app, linking paths to specific
view functions. The app provides endpoints to list ads and display ad details.

Namespaces:
    - app_name: Sets the namespace for URL names within the board app to 'board'.

URL Patterns:
    - 'ads/': Maps to the ad list view.
    - 'ads/<int:ad_id>/': Maps to the ad detail view for a specific ad by ID.
"""

# ---- Imports ----
from django.urls import path
from . import views

# ---- App Namespace ----
app_name = 'board'

# ---- URL Patterns ----
urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('ads/', views.ad_list, name='ad_list'),
    path('ads/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
]
