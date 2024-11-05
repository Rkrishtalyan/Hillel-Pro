from django.urls import path
from .views import home, about, MyView

urlpatterns = [
    path('',  home, name='home'),
    path('about/', about, name='about'),
    path('home2/', MyView.as_view(), name='home2'),
]