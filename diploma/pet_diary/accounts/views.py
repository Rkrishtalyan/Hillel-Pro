from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import translation

from accounts.forms import CustomUserCreationForm, UserProfileForm
from pets.models import Task


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            lang = request.session.get('language', 'ua')
            user.preferred_language = lang
            user.save()

            login(request, user)
            return redirect('pets:pet_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user

    # -- Task List Logic --
    show_old = request.GET.get('show_old', '0')  # '1' or '0'
    per_page = request.GET.get('per_page', '10')  # '10', '25', '50'

    if per_page not in ['10', '25', '50']:
        per_page = '10'

    tasks_qs = Task.objects.filter(
        Q(pet__owner=user) | Q(pet__caregiver=user),
        deleted_at__isnull=True
    )

    if show_old != '1':
        tasks_qs = tasks_qs.filter(status__in=['planned', 'overdue'])

    # Mass update via POST
    if request.method == 'POST' and 'bulk_update' in request.POST:
        action = request.POST.get('action')  # 'done' or 'skipped'
        task_ids = request.POST.getlist('task_ids')
        if task_ids and action in ['done', 'skipped']:
            if action == 'done':
                new_status = Task.TaskStatus.DONE
            else:
                new_status = Task.TaskStatus.SKIPPED
            Task.objects.filter(id__in=task_ids, pet__owner=user).update(status=new_status)
        return redirect(f"{reverse('accounts:profile')}?show_old={show_old}&per_page={per_page}")

    # Pagination
    tasks_qs = tasks_qs.select_related('pet').order_by('due_datetime', 'id')
    paginator = Paginator(tasks_qs, int(per_page))
    page_number = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/profile.html', {
        'user_obj': user,   # avoids conflict with template var user (auth user)
        'page_obj': page_obj,
        'show_old': show_old,
        'per_page': per_page,
    })


@login_required
def profile_edit_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'accounts/profile_edit.html', {
        'form': form,
    })


class POSTLogoutView(LogoutView):
    http_method_names = ['get', 'post', 'head', 'options']
    template_name = 'accounts/logout.html'


def set_language_view(request):
    lang = request.GET.get('lang')
    next_url = request.GET.get('next', '/')

    if lang in ['en','ru','ua']:
        if request.user.is_authenticated:
            request.user.preferred_language = lang
            request.user.save()
        else:
            # Saving into session
            request.session['language'] = lang
        translation.activate(lang)
        request.LANGUAGE_CODE = lang

    return redirect(next_url)


def set_timezone_view(request):
    tz = request.GET.get('tz')
    if tz:
        if request.user.is_authenticated:
            request.user.preferred_timezone = tz
            request.user.save()
        else:
            request.session['timezone'] = tz
    return HttpResponse("OK")
