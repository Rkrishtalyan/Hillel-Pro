from django.shortcuts import render
from django.db import connections

def home(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT 1;")
    with connections['extra'].cursor() as cursor:
        cursor.execute("SELECT 1;")
    return render(request, 'myapp/home.html')
