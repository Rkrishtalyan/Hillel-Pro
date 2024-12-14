from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Query

from tasks import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from tasks import Task


ninja_api = NinjaAPI()

@ninja_api.get('/tasks', response=list[TaskSchema])
def list_tasks(request, status=Query(None), due_date=Query(None)):
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


@ninja_api.get('/tasks/{task_id}', response=TaskSchema)
def get_task(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    return TaskSchema.from_orm(task)


@ninja_api.post('/tasks', response=TaskSchema)
def create_task(request, data: TaskCreateSchema):
    task = Task.objects.create(**data.dict())
    return TaskSchema.from_orm(task)


@ninja_api.put('/tasks/{task_id}', response=TaskSchema)
def update_task(request, task_id: int, data: TaskUpdateSchema):
    task = get_object_or_404(Task, pk=task_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    task.save()
    return TaskSchema.from_orm(task)


@ninja_api.delete('/tasks/{task_id}')
def delete_task(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return {"success": True}
