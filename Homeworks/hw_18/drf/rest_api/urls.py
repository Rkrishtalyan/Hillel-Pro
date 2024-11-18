"""
Define URL patterns for the application.

This module maps URL paths to the corresponding views, enabling API routing for
the Book-related operations and user registration. It uses a default router for
DRF viewsets and includes commented-out alternative URL patterns for potential
manual endpoint configuration.

URL Patterns:
    - Base router includes: CRUD operations for books via a viewset.
    - Explicit route for user registration.
    - Commented alternative paths for book operations.

Dependencies:
    - Django's URL configuration utilities.
    - Django REST framework's router for viewset-based endpoints.
"""
from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


router = routers.DefaultRouter()
router.register(r'book', views.BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
]

# urlpatterns = [
#     path('books/', views.BookList.as_view()),
#     path('books/<int:pk>/', views.BookDetail.as_view()),
#     path('books/create/', views.BookCreate.as_view()),
#     path('books/<int:pk>/update/', views.BookUpdate.as_view()),
#     path('books/<int:pk>/delete/', views.BookDelete.as_view()),
#     path('register/', views.UserRegisterView.as_view()),
#
# ]
