from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from user_agents import parse
from django.contrib.gis.geoip2 import GeoIP2

from shortener.forms import URLForm, RegistrationForm
from shortener.models import URL, URLClick


@login_required(login_url='login')
def home(request):
    """
    Handle the home view for creating shortened URLs.

    This view processes a URL form submitted by the user, creates or retrieves
    a shortened URL, and displays the result along with the click count.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered template with the form and results (if applicable).
    :rtype: HttpResponse
    """
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
    """
    Redirect to the original URL associated with the provided short URL.

    This view logs the click details, including device type, country, and user.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param short_url: The short URL slug to resolve.
    :type short_url: str
    :return: A redirect response to the original URL.
    :rtype: HttpResponseRedirect
    """
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
    """
    Retrieve the client's IP address from the request.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: The client's IP address.
    :rtype: str
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR', '')


def register(request):
    """
    Handle user registration.

    This view processes the registration form to create a new user account
    and log them in upon successful registration.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered template with the registration form.
    :rtype: HttpResponse
    """
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
    """
    Log out the current user and redirect to the home page.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: A redirect response to the home page.
    :rtype: HttpResponseRedirect
    """
    logout(request)
    return redirect('home')
