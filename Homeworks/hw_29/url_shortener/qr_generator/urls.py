from django.urls import path
from .views import generate_qr

app_name = 'qr_generator'

urlpatterns = [
    path('<str:short_url>/', generate_qr, name='generate_qr'),
]
