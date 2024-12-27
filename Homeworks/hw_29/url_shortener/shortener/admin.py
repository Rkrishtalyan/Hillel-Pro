from django.contrib import admin
from .models import URL, User, URLClick

admin.site.register(URL)
admin.site.register(URLClick)