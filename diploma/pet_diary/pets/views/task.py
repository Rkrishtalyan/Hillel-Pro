from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from pets.forms import TaskCreateForm, TaskEditForm
from pets.models import Pet, Task


@login_required
def create_task(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            original_task = form.save(commit=False)
            original_task.pet = pet
            original_task.created_by = request.user
            print("POST raw:", request.POST.get('due_datetime'))
            print("cleaned_data:", form.cleaned_data.get('due_datetime'))
            print(timezone.get_current_timezone())
            print(datetime.now(), datetime.utcnow())
            original_task.save()

            if (
                original_task.recurring
                and original_task.recurring_days > 0
                and original_task.due_datetime
            ):
                for i in range(1, original_task.recurring_days):  # +1
                    new_dt = original_task.due_datetime + timedelta(days=i)
                    Task.objects.create(
                        pet=pet,
                        title=original_task.title,
                        due_datetime=new_dt,
                        remind_me=original_task.remind_me,
                        remind_before=original_task.remind_before,
                        status=original_task.status,
                        # Preventing infinite loop
                        recurring=False,
                        recurring_days=0,
                        created_by=original_task.created_by,
                    )

            return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=tasks")
    else:
        form = TaskCreateForm()

    return render(request, 'pets/forms/task_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Create Task"),
    })


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    pet = task.pet
    next_url = request.GET.get('next')

    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            # old_status = task.status
            t = form.save(commit=False)
            t.mark_as_edited(request.user)
            new_status = form.cleaned_data.get('status')

            # if old_status in [Task.TaskStatus.PLANNED, Task.TaskStatus.OVERDUE] and \
               # new_status in [Task.TaskStatus.DONE, Task.TaskStatus.SKIPPED]:
            if new_status == Task.TaskStatus.DONE:
                t.mark_as_done(request.user)
            elif new_status == Task.TaskStatus.SKIPPED:
                t.mark_as_skipped(request.user)

            t.save()

            if next_url:
                return redirect(next_url)
            return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=tasks")
    else:
        form = TaskEditForm(instance=task)

    return render(request, 'pets/forms/task_form.html', {
        'form': form,
        'pet': pet,
        'task': task,
        'title': _("Edit Task"),
        'next_url': next_url,
    })


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    pet = task.pet

    if request.user != pet.owner:
        return HttpResponseForbidden("You are not allowed to delete tasks for this pet.")

    next_url = request.GET.get('next')

    if request.method == 'POST':
        task.mark_as_deleted(request.user)
        task.save()

        if next_url:
            return redirect(next_url)
        return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=tasks")

    return render(request, 'pets/task_confirm_delete.html', {
        'task': task,
        'pet': pet,
        'next_url': next_url,
    })


@login_required
def bulk_update_task_status(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        task_ids = request.POST.getlist('task_ids')
        action = request.POST.get('action')  # 'done' or 'skipped'
        if task_ids and action in ['done', 'skipped']:
            tasks = Task.objects.filter(id__in=task_ids, pet=pet, deleted_at__isnull=True)

            for t in tasks:
                t.mark_as_edited(request.user)
                if action == 'done':
                    t.mark_as_done(request.user)
                elif action == 'skipped':
                    t.mark_as_skipped(request.user)
                t.save()

        return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=tasks")

    return redirect('pets:pet_detail', pet_id=pet_id)
