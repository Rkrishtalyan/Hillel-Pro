from django.urls import path
from .views import urls_list, url_detail, rename_link

app_name = 'stats'

urlpatterns = [
    path('', urls_list, name='urls_list'),
    path('<str:short_url>/', url_detail, name='url_detail'),
    path('<str:short_url>/rename/', rename_link, name='rename_link'),
]
