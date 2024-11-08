from django.urls import path
from .views import home, about, ContactView, ServiceView

# ---- URL Patterns ----

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('service/', ServiceView.as_view(), name='service'),
]
