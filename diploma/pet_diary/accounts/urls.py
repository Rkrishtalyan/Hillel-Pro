from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import register_view, profile_view, POSTLogoutView


app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', POSTLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
]
