"""root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from web_site.views import HomePageView, RegisterView
from web_site.views_api import ArticleListCreateView, ArticleDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/articles/', ArticleListCreateView.as_view(), name='article-list-create'),
    path('api/articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
]