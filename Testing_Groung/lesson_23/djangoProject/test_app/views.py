from django.shortcuts import render

def test_page(request):
    return render(request, 'testapp/test.html')


def custom_page(request):
    return render(request, 'custom_page.html')


def home_page(request):
    return render(request, 'base.html')
