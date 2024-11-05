from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, FileResponse, HttpResponseRedirect, HttpResponseNotAllowed, JsonResponse
from django.views.generic import TemplateView

def home(request):
    return render(request, 'lesson2/home.html')

def about(request):
    return render(request, 'lesson2/about.html')

class MyView(TemplateView):
    template_name = 'lesson2/home2.html'
