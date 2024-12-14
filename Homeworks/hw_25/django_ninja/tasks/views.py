from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Query
from django.contrib.auth import authenticate
from ninja.errors import HttpError
from typing import Optional, List
from datetime import datetime

from tasks.schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema, LoginSchema, TokenSchema
from tasks.models import Task, Token
from tasks.auth import AuthBearer


ninja_api = NinjaAPI()

@ninja_api.get('/tasks', response=List[TaskSchema], auth=AuthBearer())
def list_tasks(request, status: Optional[str] = Query(None), due_date: Optional[datetime] = Query(None)):
    tasks = Task.objects.all()

    if status:
        tasks = tasks.filter(status=status)
    if due_date:
        tasks = tasks.filter(due_date=due_date)

    return [TaskSchema(
        id=task.id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        due_date=task.due_date,
        created_at=task.created_at,
        updated_at=task.updated_at,
    ) for task in tasks]


@ninja_api.get('/tasks/{task_id}', response=TaskSchema, auth=AuthBearer())
def get_task(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    return TaskSchema.from_orm(task)


@ninja_api.post('/tasks', response=TaskSchema, auth=AuthBearer())
def create_task(request, data: TaskCreateSchema):
    task = Task.objects.create(**data.dict())
    return TaskSchema.from_orm(task)


@ninja_api.put('/tasks/{task_id}', response=TaskSchema, auth=AuthBearer())
def update_task(request, task_id: int, data: TaskUpdateSchema):
    task = get_object_or_404(Task, pk=task_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    task.save()
    return TaskSchema.from_orm(task)


@ninja_api.delete('/tasks/{task_id}', auth=AuthBearer())
def delete_task(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return {"success": True}


@ninja_api.post('/login', response=TokenSchema)
def login(request, data: LoginSchema):
    user = authenticate(username=data.username, password=data.password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return {"token": str(token.key)}
    else:
        raise HttpError(401, "Invalid credentials")


@ninja_api.post('/logout', auth=AuthBearer())
def logout(request):
    user = request.auth
    token = get_object_or_404(Token, user=user)
    token.delete()
    return {"success": True}
