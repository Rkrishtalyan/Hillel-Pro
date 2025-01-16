from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.core.paginator import Paginator

from pets.models import (
    Pet,
    WeightLog,
    PetImage,
    VaccinationLog,
    Task,
    PetDocument
)
from pets.forms import (
    PetForm,
    WeightLogForm,
    PetImageForm,
    VaccinationLogForm,
    TaskCreateForm,
    TaskEditForm,
    PetDocumentForm
)


# ------------------------------------------------
#                PET CRUD
# ------------------------------------------------

@login_required
def pet_list(request):
    view_mode = request.GET.get('view', 'list')
    pets = Pet.objects.all().order_by('name')
    return render(request, 'pets/pet_list.html', {
        'pets': pets,
        'view_mode': view_mode,
    })


@login_required
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    active_tab = request.GET.get('tab', 'tasks')

    weight_logs = pet.weight_logs.order_by('-date')
    photos = pet.images.order_by('-uploaded_at')
    vaccinations = pet.vaccination_logs.order_by('-date_administered')
    documents = pet.documents.all()

    # ------------------------------
    # Task List Logic (TAB=tasks)
    # ------------------------------
    show_old = request.GET.get('show_old', '0')  # '0' or '1'
    per_page = request.GET.get('per_page', '10')  # '10', '25', '50'
    if per_page not in ['10', '25', '50']:
        per_page = '10'

    # Base queryset
    tasks_qs = pet.tasks.all()

    # Hiding old tasks (done/skipped)
    if show_old != '1':
        tasks_qs = tasks_qs.filter(status__in=['planned', 'overdue'])

    # Mass status update
    if request.method == 'POST' and active_tab == 'tasks':
        if 'bulk_update' in request.POST:
            action = request.POST.get('action')  # 'done' or 'skipped'
            task_ids = request.POST.getlist('task_ids')
            if task_ids and action in ['done', 'skipped']:
                from pets.models import Task
                new_status = Task.TaskStatus.DONE if action == 'done' else Task.TaskStatus.SKIPPED
                Task.objects.filter(id__in=task_ids, pet=pet).update(status=new_status)
            # Redirect with saved params
            return redirect(
                f"{reverse('pets:pet_detail', args=[pet_id])}"
                + f"?tab=tasks&show_old={show_old}&per_page={per_page}"
            )

    # Pagination
    tasks_qs = tasks_qs.order_by('due_date', 'due_time', 'id')
    paginator = Paginator(tasks_qs, int(per_page))
    page_number = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)

    # --Context--
    context = {
        'pet': pet,
        'active_tab': active_tab,

        # For other tabs
        'weight_logs': weight_logs,
        'photos': photos,
        'vaccinations': vaccinations,
        'documents': documents,

        # For tasks tab
        'page_obj': page_obj,
        'show_old': show_old,
        'per_page': per_page,
    }

    return render(request, 'pets/pet_detail.html', context)


@login_required
def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('pets:pet_detail', pet_id=pet.id)
    else:
        form = PetForm()
    return render(request, 'pets/pet_form.html', {
        'form': form,
        'title': _("Create Pet"),
    })


@login_required
def pet_update(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pets:pet_detail', pet_id=pet.id)
    else:
        form = PetForm(instance=pet)

    return render(request, 'pets/pet_form.html', {
        'form': form,
        'title': _("Edit Pet"),
        'pet': pet,
    })


@login_required
def pet_delete(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        pet.delete()
        return redirect('pets:pet_list')
    return render(request, 'pets/pet_confirm_delete.html', {'pet': pet})


# ------------------------------------------------
#                TASKS
# ------------------------------------------------

@login_required
def task_create(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            original_task = form.save(commit=False)
            original_task.pet = pet
            original_task.save()

            # Creating copies for recurring tasks
            if original_task.recurring and original_task.recurring_days > 0 and original_task.due_date:
                for i in range(1, original_task.recurring_days + 1):
                    new_date = original_task.due_date + timedelta(days=i)
                    Task.objects.create(
                        pet=pet,
                        title=original_task.title,
                        due_date=new_date,
                        due_time=original_task.due_time,
                        remind_me=original_task.remind_me,
                        remind_before=original_task.remind_before,
                        status=original_task.status,
                        # Preventing infinite loop
                        recurring=False,
                        recurring_days=0,
                    )

            return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=tasks")
    else:
        form = TaskCreateForm()

    return render(request, 'pets/task_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Create Task"),
    })


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    pet = task.pet
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=tasks")
    else:
        form = TaskEditForm(instance=task)

    return render(request, 'pets/task_form.html', {
        'form': form,
        'pet': pet,
        'task': task,
        'title': _("Edit Task"),
    })


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    pet = task.pet
    if request.method == 'POST':
        task.delete()
        return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=tasks")
    return render(request, 'pets/task_confirm_delete.html', {
        'task': task,
        'pet': pet
    })


@login_required
def task_bulk_status(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        task_ids = request.POST.getlist('task_ids')
        action = request.POST.get('action')  # 'done' or 'skipped'
        if task_ids and action in ['done', 'skipped']:
            if action == 'done':
                new_status = Task.TaskStatus.DONE
            else:
                new_status = Task.TaskStatus.SKIPPED

            Task.objects.filter(id__in=task_ids, pet=pet).update(status=new_status)

        return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=tasks")

    return redirect('pets:pet_detail', pet_id=pet_id)


# ------------------------------------------------
#                WEIGHT LOG
# ------------------------------------------------

@login_required
def weight_create(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = WeightLogForm(request.POST)
        if form.is_valid():
            wl = form.save(commit=False)
            wl.pet = pet
            wl.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=weight")
    else:
        form = WeightLogForm()

    return render(request, 'pets/weight_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Add Weight"),
    })


@login_required
def weight_edit(request, weight_id):
    wl = get_object_or_404(WeightLog, id=weight_id)
    pet = wl.pet
    if request.method == 'POST':
        form = WeightLogForm(request.POST, instance=wl)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=weight")
    else:
        form = WeightLogForm(instance=wl)

    return render(request, 'pets/weight_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Edit Weight"),
        'weight_log': wl,
    })


# ------------------------------------------------
#                PHOTOS
# ------------------------------------------------

@login_required
def photo_upload(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = PetImageForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.pet = pet
            photo.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=photos")
    else:
        form = PetImageForm()

    return render(request, 'pets/photo_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Upload Photo"),
    })


# ------------------------------------------------
#                VACCINATIONS
# ------------------------------------------------

@login_required
def vaccination_create(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = VaccinationLogForm(request.POST)
        if form.is_valid():
            vac = form.save(commit=False)
            vac.pet = pet
            vac.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=vaccinations")
    else:
        form = VaccinationLogForm()

    return render(request, 'pets/vaccination_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Add Vaccination"),
    })


@login_required
def vaccination_edit(request, vacc_id):
    vac = get_object_or_404(VaccinationLog, id=vacc_id)
    pet = vac.pet
    if request.method == 'POST':
        form = VaccinationLogForm(request.POST, instance=vac)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=vaccinations")
    else:
        form = VaccinationLogForm(instance=vac)

    return render(request, 'pets/vaccination_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Edit Vaccination"),
        'vaccination': vac,
    })


# ------------------------------------------------
#                DOCUMENTS
# ------------------------------------------------

@login_required
def document_upload(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = PetDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.pet = pet
            doc.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=documents")
    else:
        form = PetDocumentForm()

    return render(request, 'pets/document_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Add Document"),
    })


@login_required
def document_edit(request, doc_id):
    doc = get_object_or_404(PetDocument, id=doc_id)
    pet = doc.pet
    if request.method == 'POST':
        form = PetDocumentForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=documents")
    else:
        form = PetDocumentForm(instance=doc)

    return render(request, 'pets/document_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Edit Document"),
        'document': doc,
    })
