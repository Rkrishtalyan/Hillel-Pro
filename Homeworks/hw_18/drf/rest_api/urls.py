from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


# router = routers.DefaultRouter()
# router.register(r'books', views.BookList.as_view())
# router.register(r'books/<int:pk>', views.BookDetail.as_view())
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = [
    path('books/', views.BookList.as_view()),
    path('books/<int:pk>/', views.BookDetail.as_view()),
    path('books/create/', views.BookCreate.as_view()),
    path('books/<int:pk>/update/', views.BookUpdate.as_view()),
    path('books/<int:pk>/delete/', views.BookDelete.as_view()),
    path('register/', views.UserRegisterView.as_view()),

]
