from django.shortcuts import render, redirect, get_object_or_404
from .forms import URLForm, RegistrationForm
from .models import URL, URLClick
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            url, created = URL.objects.get_or_create(
                original_url=original_url,
                created_by=request.user if request.user.is_authenticated else None
            )
            if created:
                url.save()
            clicks = url.clicks.count()
            return render(
                request,
                'shortener/home.html',
                context={
                    'short_url': request.build_absolute_uri(url.short_url),
                    'clicks': clicks
                }
            )
    else:
        form = URLForm()
    return render(request, 'shortener/home.html', {'form': form})


def redirect_to_url(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)
    URLClick.objects.create(url=url, user=request.user if request.user.is_authenticated else None)
    return redirect(url.original_url)


@login_required
def user_statistics(request):
    urls = URL.objects.filter(created_by=request.user)
    return render(request, 'shortener/statistics.html', {'urls': urls})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'shortener/register.html', {'form': form})
