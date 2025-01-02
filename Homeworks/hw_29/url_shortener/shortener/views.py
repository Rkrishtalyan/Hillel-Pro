from django.shortcuts import render, redirect, get_object_or_404
from .forms import URLForm, RegistrationForm
from .models import URL, URLClick
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from user_agents import parse
from django.contrib.gis.geoip2 import GeoIP2


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
                    'clicks': clicks,
                    'short_url_slug': url.short_url
                }
            )
    else:
        form = URLForm()
    return render(request, 'shortener/home.html', {'form': form})


def redirect_to_url(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)

    user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
    if user_agent.is_mobile:
        device_type = 'Mobile'
    elif user_agent.is_tablet:
        device_type = 'Tablet'
    elif user_agent.is_pc:
        device_type = 'Desktop'
    else:
        device_type = 'Unknown'

    ip_address = get_client_ip(request)
    try:
        geo = GeoIP2()
        country = geo.country_name(ip_address)
    except:
        country = 'Unknown'

    URLClick.objects.create(
        url=url,
        user=request.user if request.user.is_authenticated else None,
        device_type=device_type,
        country=country
    )

    return redirect(url.original_url)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR', '')


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


def logout_user(request):
    logout(request)
    return redirect('home')
