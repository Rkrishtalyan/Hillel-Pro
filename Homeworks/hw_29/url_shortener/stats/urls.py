from django.urls import path
from .views import urls_list, url_detail

app_name = 'stats'

urlpatterns = [
    path('', urls_list, name='urls_list'),
    path('<str:short_url>/', url_detail, name='url_detail'),
]