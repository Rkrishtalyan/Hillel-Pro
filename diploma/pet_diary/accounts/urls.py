from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import (
    register_view,
    profile_view,
    POSTLogoutView,
    profile_edit_view,
    set_language_view,
    set_timezone_view,
)


app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', POSTLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('set-language/', set_language_view, name='set_language'),
    path('set-timezone/', set_timezone_view, name='set_timezone'),
]
