from django.urls import path, re_path
from . import views

# ---- URL Patterns Configuration ----
urlpatterns = [
    path('', views.home, name='home'),
    # Displays the home page

    path('about/', views.about, name='about'),
    # Displays the about page

    path('contact/', views.contact, name='contact'),
    # Displays the contact page

    re_path(r'^post/(?P<id>[0-9]+)/$', views.post_view, name='post_view'),
    # Displays a specific post by ID

    re_path(r'^profile/(?P<username>[A-Za-z]+)/$', views.profile_view, name='profile_view'),
    # Displays user profile by username

    re_path(
        r'^event/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/$',
        views.event_view,
        name='event_view'
    ),
    # Displays event details for a specific date (year, month, day)


]
