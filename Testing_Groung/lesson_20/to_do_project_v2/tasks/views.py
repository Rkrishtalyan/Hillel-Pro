from django.shortcuts import render
from django.core.mail import send_mail
import csv
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Task
import logging


logger = logging.getLogger(__name__)


def task_list(request):
    logger.info('task list viewed')
    tasks = Task.objects.all()
    data = {'task': list(tasks.values('id', 'title', 'completed'))}
    return JsonResponse(data)


def send_task_notification(task_title):
    send_mail(
        'new_task_created',
        f'task {task_title} created',
        'example@gmail.com',
        ['email1@gmail.com','email2@gmail.com','email3@gmail.com'],
    )


@login_required
def task_list_v2(request):
    tasks = Task.objects.filter(user=request.user)
    return JsonResponse({'tasks': list(tasks.values('id', 'title', 'completed'))})


def export_tasks_csv(request):
    tasks = Task.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'title', 'completed'])
    for task in tasks:
        writer.writerow([task.id, task.title, task.completed])
    return response


