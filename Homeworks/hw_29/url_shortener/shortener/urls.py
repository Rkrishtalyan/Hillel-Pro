from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', LoginView.as_view(template_name='shortener/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('go/<str:short_url>/', views.redirect_to_url, name='redirect_to_url'),
]
