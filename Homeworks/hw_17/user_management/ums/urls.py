from django.urls import path
from . import views

# ---- URL Patterns for Application ----
urlpatterns = [
    # Default Path
    path('', views.login_view, name='login'),

    # Login and Logout Views
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Registration and Profile Management Views
    path('register/', views.register_view, name='register'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('change_password/', views.change_password_view, name='change_password'),

    # Profile View
    path('profile/<str:username>/', views.profile_view, name='profile_view'),

]
