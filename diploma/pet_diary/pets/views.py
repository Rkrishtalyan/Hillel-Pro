import mimetypes
from tkinter import Image

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from datetime import timedelta, datetime
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpResponseForbidden, FileResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import os

from pets.notifications import _notify_owner_about_result
from pets.utils import send_telegram_message


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
    view_mode = request.GET.get('view', 'gallery')

    if view_mode == 'gallery':
        per_page = request.GET.get('per_page_gallery', '12')
        per_page_options = ['12', '24', '48']
        if per_page not in per_page_options:
            per_page = '12'
    else:
        per_page = request.GET.get('per_page_list', '10')
        per_page_options = ['10', '25', '50']
        if per_page not in per_page_options:
            per_page = '10'

    pets_qs = Pet.objects.filter(
        models.Q(owner=request.user) | models.Q(caregiver=request.user)
    ).order_by('name')

    paginator = Paginator(pets_qs, int(per_page))
    page_number = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)

    context = {
        'pets': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'view_mode': view_mode,
        'per_page': per_page,
        'per_page_options': per_page_options,
    }

    return render(request, 'pets/pet_list.html', context)


@login_required
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    active_tab = request.GET.get('tab', 'tasks')

    # ------------------------------
    # Weight Logs Pagination (TAB=weight)
    # ------------------------------
    per_page_weight = request.GET.get('per_page_weight', '10')
    if per_page_weight not in ['10', '25', '50']:
        per_page_weight = '10'
    weight_logs_qs = pet.weight_logs.filter(deleted_at__isnull=True).order_by('-date')
    paginator_weight = Paginator(weight_logs_qs, int(per_page_weight))
    page_number_weight = request.GET.get('page_weight', '1')
    page_obj_weight = paginator_weight.get_page(page_number_weight)

    # ------------------------------
    # Tasks Pagination (TAB=tasks)
    # ------------------------------
    show_old = request.GET.get('show_old', '0')  # '0' or '1'
    per_page_tasks = request.GET.get('per_page_tasks', '10')  # '10', '25', '50'
    if per_page_tasks not in ['10', '25', '50']:
        per_page_tasks = '10'

    tasks_qs = pet.tasks.filter(deleted_at__isnull=True)

    # Hiding old tasks (done/skipped)
    if show_old != '1':
        tasks_qs = tasks_qs.filter(status__in=['planned', 'overdue'])

    tasks_qs = tasks_qs.order_by('due_datetime', 'id')
    paginator_tasks = Paginator(tasks_qs, int(per_page_tasks))
    page_number_tasks = request.GET.get('page_tasks', '1')
    page_obj_tasks = paginator_tasks.get_page(page_number_tasks)

    # ------------------------------
    # Vaccinations Pagination (TAB=vaccinations)
    # ------------------------------
    per_page_vaccinations = request.GET.get('per_page_vaccinations', '10')
    if per_page_vaccinations not in ['10', '25', '50']:
        per_page_vaccinations = '10'
    vaccinations_qs = pet.vaccination_logs.filter(deleted_at__isnull=True).order_by('-date_administered')
    paginator_vaccinations = Paginator(vaccinations_qs, int(per_page_vaccinations))
    page_number_vaccinations = request.GET.get('page_vaccinations', '1')
    page_obj_vaccinations = paginator_vaccinations.get_page(page_number_vaccinations)

    # ------------------------------
    # Documents Pagination (TAB=documents)
    # ------------------------------
    per_page_documents = request.GET.get('per_page_documents', '10')
    if per_page_documents not in ['10', '25', '50']:
        per_page_documents = '10'
    documents_qs = pet.documents.filter(deleted_at__isnull=True).order_by('-doc_date')
    paginator_documents = Paginator(documents_qs, int(per_page_documents))
    page_number_documents = request.GET.get('page_documents', '1')
    page_obj_documents = paginator_documents.get_page(page_number_documents)

    # ------------------------------
    # Photos Pagination (TAB=photos)
    # ------------------------------
    view_mode_photos = request.GET.get('view_photos', 'gallery')  # 'gallery' или 'list'
    per_page_photos = request.GET.get('per_page_photos', '12')  # '12', '24', '48'
    if per_page_photos not in ['12', '24', '48']:
        per_page_photos = '12'

    photos_qs = pet.images.filter(deleted_at__isnull=True).order_by('-uploaded_at')

    paginator_photos = Paginator(photos_qs, int(per_page_photos))
    page_number_photos = request.GET.get('page_photos', '1')
    page_obj_photos = paginator_photos.get_page(page_number_photos)

    # Determine view mode (gallery or list)
    if view_mode_photos not in ['gallery', 'list']:
        view_mode_photos = 'gallery'

    # --Context--
    context = {
        'pet': pet,
        'active_tab': active_tab,

        # For other tabs
        'weight_logs': page_obj_weight.object_list,
        'page_obj_weight': page_obj_weight,
        'vaccinations': page_obj_vaccinations.object_list,
        'page_obj_vaccinations': page_obj_vaccinations,
        'documents': page_obj_documents.object_list,
        'page_obj_documents': page_obj_documents,

        # For tasks tab
        'tasks': page_obj_tasks.object_list,
        'page_obj_tasks': page_obj_tasks,
        'show_old': show_old,
        'per_page_tasks': per_page_tasks,

        # For photos tab
        'photos': page_obj_photos.object_list,
        'page_obj_photos': page_obj_photos,
        'view_mode_photos': view_mode_photos,
        'per_page_photos': per_page_photos,

        'form': PetImageForm(),
    }

    return render(request, 'pets/pet_detail.html', context)


@login_required
def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.created_by = request.user
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
            try:
                p = form.save(commit=False)
                p.mark_as_edited(request.user)
                p.save()
                return redirect('pets:pet_detail', pet_id=pet.id)
            except ValidationError as e:
                form.add_error('caregiver_email', e)
    else:
        form = PetForm(instance=pet, initial={
            'caregiver_email': pet.caregiver.email if pet.caregiver else ''
        })

    return render(request, 'pets/pet_form.html', {
        'form': form,
        'title': _("Edit Pet"),
        'pet': pet,
    })


@login_required
def pet_delete(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        pet.mark_as_deleted(request.user)
        tasks = Task.objects.filter(pet=pet, deleted_at__isnull=True)
        for t in tasks:
            t.mark_as_deleted(request.user)
        weight_records = WeightLog.objects.filter(pet=pet, deleted_at__isnull=True)
        for w in weight_records:
            w.mark_as_deleted(request.user)
        vaccinations = VaccinationLog.objects.filter(pet=pet, deleted_at__isnull=True)
        for v in vaccinations:
            v.mark_as_deleted(request.user)
        images = PetImage.objects.filter(pet=pet, deleted_at__isnull=True)
        for i in images:
            i.path.delete(save=False)
            i.mark_as_deleted(request.user)
            i.path.name = 'pet_images/deleted_image.jpg'
            i.save()
        documents = PetDocument.objects.filter(pet=pet, deleted_at__isnull=True)
        for d in documents:
            d.doc_file.delete(save=False)
            d.mark_as_deleted(request.user)
            d.doc_file.name = 'pet_documents/deleted_document.pdf'
            d.save()

        pet.save()
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

    return render(request, 'pets/task_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Create Task"),
    })


@login_required
def task_edit(request, task_id):
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

    return render(request, 'pets/task_form.html', {
        'form': form,
        'pet': pet,
        'task': task,
        'title': _("Edit Task"),
        'next_url': next_url,
    })


@login_required
def task_delete(request, task_id):
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
def task_bulk_status(request, pet_id):
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


# ------------------------------------------------
#                WEIGHT LOG
# ------------------------------------------------

@login_required
def weight_create(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = WeightLogForm(request.POST)
        if form.is_valid():
            w = form.save(commit=False)
            w.pet = pet
            w.created_by = request.user
            w.save()
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

    if request.user != pet.owner and request.user != pet.caregiver:
        return HttpResponseForbidden("You are not allowed to edit weight logs for this pet.")

    if request.method == 'POST':
        form = WeightLogForm(request.POST, instance=wl)
        if form.is_valid():
            w = form.save(commit=False)
            w.mark_as_edited(request.user)
            w.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=weight")
    else:
        form = WeightLogForm(instance=wl)

    return render(request, 'pets/weight_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Edit Weight"),
        'weight_log': wl,
    })


@login_required
def weight_delete(request, weight_id):
    weight_log = get_object_or_404(WeightLog, id=weight_id)
    pet = weight_log.pet

    if request.user != pet.owner:
        return HttpResponseForbidden("You are not allowed to delete weight logs for this pet.")

    if request.method == 'POST':
        weight_log.mark_as_deleted(request.user)
        weight_log.save()
        return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=weight")

    return render(request, 'pets/weight_confirm_delete.html', {
        'weight_log': weight_log,
        'pet': pet
    })


# ------------------------------------------------
#                PHOTOS
# ------------------------------------------------

@login_required
def upload_pet_image(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = PetImageForm(request.POST, request.FILES)
        if form.is_valid():
            pet_image = form.save(commit=False)
            pet_image.pet = pet
            pet_image.image_name = pet_image.path.name
            pet_image.created_by = request.user
            if PetImage.objects.filter(pet=pet, path=request.FILES['path']).exists():
                messages.error(request, "Such image already exists.")
            else:
                pet_image.save()
                messages.success(request, "Photo uploaded successfully.")

                tab = request.POST.get('tab', 'photos')
                view_photos = request.POST.get('view_photos', 'gallery')
                per_page_photos = request.POST.get('per_page_photos', '12')
                page_photos = request.POST.get('page_photos', '1')

                query_params = f"?tab={tab}&view_photos={view_photos}&per_page_photos={per_page_photos}&page_photos={page_photos}"
                return redirect(reverse('pets:pet_detail', args=[pet.id]) + query_params)
        else:
            messages.error(request, "Failed to upload photo. Please correct the errors below.")
    else:
        form = PetImageForm()

    context = {
        'form': form,
        'pet': pet,
    }
    return render(request, 'pets/photo_form.html', context)


@login_required
def edit_pet_image(request, pet_id, image_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet_image = get_object_or_404(PetImage, id=image_id, pet=pet, deleted_at__isnull=True)

    if request.user != pet.owner and request.user != pet.caregiver:
        return HttpResponseForbidden(_("You do not have permission to edit this image."))

    if request.method == 'POST':
        form = PetImageForm(request.POST, request.FILES, instance=pet_image)
        if form.is_valid():
            if 'path' in form.changed_data:
                if PetImage.objects.filter(pet=pet, path=request.FILES.get('path')).exclude(id=image_id).exists():
                    messages.error(request, _("Such image already exists."))
                    return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=photos&view_photos={request.POST.get('view_photos', 'gallery')}&per_page_photos={request.POST.get('per_page_photos', '12')}&page_photos={request.POST.get('page_photos', '1')}")
            form.save()
            messages.success(request, _("Image has been successfully updated."))

            tab = request.POST.get('tab', 'photos')
            view_photos = request.POST.get('view_photos', 'gallery')
            per_page_photos = request.POST.get('per_page_photos', '12')
            page_photos = request.POST.get('page_photos', '1')

            query_params = f"?tab={tab}&view_photos={view_photos}&per_page_photos={per_page_photos}&page_photos={page_photos}"
            return redirect(reverse('pets:pet_detail', args=[pet.id]) + query_params)
        else:
            messages.error(request, _("Failed to update image. Please correct the errors below."))
    else:
        form = PetImageForm(instance=pet_image)
        tab = request.GET.get('tab', 'photos')
        view_photos = request.GET.get('view_photos', 'gallery')
        per_page_photos = request.GET.get('per_page_photos', '12')
        page_photos = request.GET.get('page_photos', '1')

    context = {
        'form': form,
        'pet': pet,
        'title': _("Edit Image"),
        'pet_image': pet_image,
        'tab': tab if request.method == 'GET' else request.POST.get('tab', 'photos'),
        'view_photos': view_photos if request.method == 'GET' else request.POST.get('view_photos', 'gallery'),
        'per_page_photos': per_page_photos if request.method == 'GET' else request.POST.get('per_page_photos', '12'),
        'page_photos': page_photos if request.method == 'GET' else request.POST.get('page_photos', '1'),
    }
    return render(request, 'pets/photo_form.html', context)



@login_required
def download_pet_image(request, pet_id, image_name):
    pet = get_object_or_404(Pet, id=pet_id)

    if pet.owner != request.user and pet.caregiver != request.user:
        return HttpResponseForbidden("You do not have permission to access this file.")

    try:
        image = PetImage.objects.get(pet=pet, image_name=image_name, deleted_at__isnull=True)
    except PetImage.DoesNotExist:
        return HttpResponseForbidden("File not found.")

    file_path = os.path.join(settings.MEDIA_ROOT, image.path.name)
    if not os.path.exists(file_path):
        return HttpResponseForbidden("File not found.")

    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = 'application/octet-stream'

    download = request.GET.get('download', '0')

    if download == '1':
        disposition = f'attachment; filename="{os.path.basename(file_path)}"'
    else:
        disposition = f'inline; filename="{os.path.basename(file_path)}"'

    try:
        file_handle = open(file_path, 'rb')
        response = FileResponse(file_handle, content_type=mime_type)
        response['Content-Disposition'] = disposition
        return response
    except Exception as e:
        return HttpResponseForbidden("Error accessing the file.")


@login_required
def delete_pet_image(request, pet_id, image_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if pet.owner != request.user and pet.caregiver != request.user:
        return HttpResponseForbidden(_("You do not have permission to delete this image."))

    pet_image = get_object_or_404(PetImage, id=image_id, pet=pet, deleted_at__isnull=True)

    tab = request.GET.get('tab', 'photos') if request.method == 'GET' else request.POST.get('tab', 'photos')
    view_photos = request.GET.get('view_photos', 'gallery') if request.method == 'GET' else request.POST.get('view_photos', 'gallery')
    per_page_photos = request.GET.get('per_page_photos', '12') if request.method == 'GET' else request.POST.get('per_page_photos', '12')
    page_photos = request.GET.get('page_photos', '1') if request.method == 'GET' else request.POST.get('page_photos', '1')

    if request.method == 'POST':
        pet_image.path.delete(save=False)
        pet_image.mark_as_deleted(request.user)
        pet_image.path.name = 'pet_images/deleted_image.jpg'
        pet_image.save()
        messages.success(request, _("Image has been successfully deleted."))

        tab = request.POST.get('tab', 'photos')
        view_photos = request.POST.get('view_photos', 'gallery')
        per_page_photos = request.POST.get('per_page_photos', '12')
        page_photos = request.POST.get('page_photos', '1')

        query_params = f"?tab={tab}&view_photos={view_photos}&per_page_photos={per_page_photos}&page_photos={page_photos}"
        return redirect(reverse('pets:pet_detail', args=[pet.id]) + query_params)
    else:
        return render(request, 'pets/image_confirm_delete.html', {
            'pet_image': pet_image,
            'pet': pet,
            'tab': tab,
            'view_photos': view_photos,
            'per_page_photos': per_page_photos,
            'page_photos': page_photos,
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
            vac.created_by = request.user
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
    vac = get_object_or_404(VaccinationLog, id=vacc_id, deleted_at__isnull=True)
    pet = vac.pet

    if request.user != pet.owner and request.user != pet.caregiver:
        return HttpResponseForbidden("You are not allowed to edit vaccination logs for this pet.")

    if request.method == 'POST':
        form = VaccinationLogForm(request.POST, request.FILES, instance=vac)
        if form.is_valid():
            v = form.save(commit=False)
            v.mark_as_edited(request.user)
            v.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=vaccinations")
    else:
        form = VaccinationLogForm(instance=vac)

    return render(request, 'pets/vaccination_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Edit Vaccination"),
        'vaccination': vac,
    })


@login_required
def vaccination_delete(request, vacc_id):
    vaccination_log = get_object_or_404(VaccinationLog, id=vacc_id, deleted_at__isnull=True)
    pet = vaccination_log.pet

    if request.user != pet.owner:
        return HttpResponseForbidden("You are not allowed to delete vaccination logs for this pet.")

    if request.method == 'POST':
        vaccination_log.mark_as_deleted(request.user)
        vaccination_log.save()
        return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=vaccinations")

    return render(request, 'pets/vaccination_confirm_delete.html', {
        'vaccination_log': vaccination_log,
        'pet': pet
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
            doc.doc_file_name = doc.doc_file.name
            doc.created_by = request.user
            if PetDocument.objects.filter(pet=pet, doc_file=request.FILES['doc_file']).exists():
                messages.error(request, "This document already exists.")
            else:
                doc.save()
                messages.success(request, _("Document uploaded successfully."))
                return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=documents")
        else:
            messages.error(request, "Failed to upload document. Please correct the errors below.")
    else:
        form = PetDocumentForm()

    context = {
        'form': form,
        'pet': pet,
        'title': _("Add Document"),
    }
    return render(request, 'pets/document_form.html', context)


@login_required
def document_edit(request, doc_id):
    doc = get_object_or_404(PetDocument, id=doc_id, deleted_at__isnull=True)
    pet = doc.pet
    if request.method == 'POST':
        form = PetDocumentForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            d = form.save(commit=False)
            d.mark_as_edited(request.user)
            d.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=documents")
    else:
        form = PetDocumentForm(instance=doc)

    return render(request, 'pets/document_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Edit Document"),
        'document': doc,
    })


@login_required
def delete_pet_document(request, pet_id, doc_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if pet.owner != request.user and pet.caregiver != request.user:
        return HttpResponseForbidden(_("You do not have permission to delete this document."))

    pet_document = get_object_or_404(PetDocument, id=doc_id, pet=pet, deleted_at__isnull=True)

    if request.method == 'POST':
        pet_document.doc_file.delete(save=False)
        pet_document.mark_as_deleted(request.user)
        pet_document.doc_file.name = 'pet_documents/deleted_document.pdf'
        pet_document.save()
        messages.success(request, _("Document has been successfully deleted."))

        return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=documents")
    else:
        return render(request, 'pets/document_confirm_delete.html', {
            'pet_document': pet_document,
            'pet': pet
        })


@login_required
def protected_media_document(request, pet_id, doc_name):
    pet = get_object_or_404(Pet, id=pet_id)

    if pet.owner != request.user and pet.caregiver != request.user:
        return HttpResponseForbidden("You do not have permission to access this file.")

    try:
        document = PetDocument.objects.get(pet=pet, doc_file_name=doc_name, deleted_at__isnull=True)
    except PetDocument.DoesNotExist:
        return HttpResponseForbidden("File not found.")

    file_path = os.path.join(settings.MEDIA_ROOT, document.doc_file.name)
    if not os.path.exists(file_path):
        return HttpResponseForbidden("File not found.")

    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = 'application/octet-stream'

    download = request.GET.get('download', '0')

    if download == '1':
        disposition = f'attachment; filename="{os.path.basename(file_path)}"'
    else:
        disposition = f'inline; filename="{os.path.basename(file_path)}"'

    try:
        file_handle = open(file_path, 'rb')
        response = FileResponse(file_handle, content_type=mime_type)
        response['Content-Disposition'] = disposition
        return response
    except Exception as e:
        return HttpResponseForbidden("Error accessing the file.")
