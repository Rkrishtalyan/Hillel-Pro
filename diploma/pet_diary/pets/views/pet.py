from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from pets.forms import PetImageForm, PetForm
from pets.models import Pet, Task, WeightRecord, Vaccination, PetImage, PetDocument


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
    weight_logs_qs = pet.weight_records.filter(deleted_at__isnull=True).order_by('-date')
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
    vaccinations_qs = pet.vaccination.filter(deleted_at__isnull=True).order_by('-date_administered')
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

        # For other pet_detail_tabs
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


# ------------------------------------------------
#                PET CRUD
# ------------------------------------------------


@login_required
def create_pet(request):
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
    return render(request, 'pets/forms/pet_form.html', {
        'form': form,
        'title': _("Create Pet"),
    })


@login_required
def edit_pet(request, pet_id):
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

    return render(request, 'pets/forms/pet_form.html', {
        'form': form,
        'title': _("Edit Pet"),
        'pet': pet,
    })


@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        pet.mark_as_deleted(request.user)
        tasks = Task.objects.filter(pet=pet, deleted_at__isnull=True)
        for t in tasks:
            t.mark_as_deleted(request.user)
        weight_records = WeightRecord.objects.filter(pet=pet, deleted_at__isnull=True)
        for w in weight_records:
            w.mark_as_deleted(request.user)
        vaccinations = Vaccination.objects.filter(pet=pet, deleted_at__isnull=True)
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
