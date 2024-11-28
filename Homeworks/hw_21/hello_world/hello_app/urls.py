from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_user_profiles/', views.get_user_profiles, name='get_user_profiles'),
]
