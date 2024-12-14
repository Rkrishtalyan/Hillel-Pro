from django.urls import path
from tasks import views

urlpatterns = [
    path('api/', views.ninja_api.urls)
]