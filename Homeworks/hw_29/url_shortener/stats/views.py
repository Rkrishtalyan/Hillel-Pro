from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from shortener.models import URL


@login_required
def rename_link(request, short_url):
    url_obj = get_object_or_404(URL, short_url=short_url, created_by=request.user)
    if request.method == 'POST':
        new_name = request.POST.get('custom_name', '').strip()
        url_obj.custom_name = new_name or None
        url_obj.save()
        return redirect('stats:url_detail', short_url=short_url)
    return redirect('stats:url_detail', short_url=short_url)


@login_required
def urls_list(request):
    user_urls = URL.objects.filter(created_by=request.user)
    return render(request, 'stats/urls_list.html', {'user_urls': user_urls})


@login_required
def url_detail(request, short_url):
    url_obj = get_object_or_404(URL, short_url=short_url, created_by=request.user)
    full_short_url = request.build_absolute_uri(f'/go/{url_obj.short_url}')

    clicks_qs = url_obj.clicks.all()

    selected_period = request.GET.get('period', 'all')

    if selected_period == 'hour':
        # Last 1 hour
        cutoff = timezone.now() - timedelta(hours=1)
        clicks_qs = clicks_qs.filter(clicked_at__gte=cutoff)
    elif selected_period == 'day':
        # Last 24 hours
        cutoff = timezone.now() - timedelta(days=1)
        clicks_qs = clicks_qs.filter(clicked_at__gte=cutoff)
    elif selected_period == 'month':
        # Last 30 days
        cutoff = timezone.now() - timedelta(days=30)
        clicks_qs = clicks_qs.filter(clicked_at__gte=cutoff)

    clicks_count = clicks_qs.count()

    device_rows = (
        clicks_qs
        .values('device_type')
        .annotate(num_clicks=Count('device_type'))
    )
    device_stats = []
    for row in device_rows:
        pct = 0
        if clicks_count > 0:
            pct = (row['num_clicks'] / clicks_count) * 100
        device_stats.append({
            'device_type': row['device_type'],
            'num_clicks': row['num_clicks'],
            'percentage': pct
        })

    country_rows = (
        clicks_qs
        .values('country')
        .annotate(num_clicks=Count('country'))
        .order_by('-num_clicks')
    )
    country_stats = []
    for row in country_rows:
        pct = 0
        if clicks_count > 0:
            pct = (row['num_clicks'] / clicks_count) * 100
        country_stats.append({
            'country': row['country'],
            'num_clicks': row['num_clicks'],
            'percentage': pct
        })

    context = {
        'url_obj': url_obj,
        'clicks_count': clicks_count,
        'device_stats': device_stats,
        'country_stats': country_stats,
        'selected_period': selected_period,
        'full_short_url': full_short_url,
    }
    return render(request, 'stats/url_detail.html', context)
