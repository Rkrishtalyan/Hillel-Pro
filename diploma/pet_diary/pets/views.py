from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
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
    TaskForm,
    PetDocumentForm
)


@login_required
def pet_list(request):
    pets = Pet.objects.all()
    return render(request, 'pets/pet_list.html', {'pets': pets})


@login_required
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST' and 'weight_submit' in request.POST:
        weight_form = WeightLogForm(request.POST)
        if weight_form.is_valid():
            weight_log = weight_form.save(commit=False)
            weight_log.pet = pet
            weight_log.save()
            return redirect('pets:pet_detail', pet_id=pet.id)
    else:
        weight_form = WeightLogForm()

    if request.method == 'POST' and 'photo_submit' in request.POST:
        photo_form = PetImageForm(request.POST, request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.pet = pet
            photo.save()
            return redirect('pets:pet_detail', pet_id=pet.id)
    else:
        photo_form = PetImageForm()

    if request.method == 'POST' and 'vaccine_submit' in request.POST:
        vaccine_form = VaccinationLogForm(request.POST)
        if vaccine_form.is_valid():
            vaccination = vaccine_form.save(commit=False)
            vaccination.pet = pet
            vaccination.save()
            return redirect('pets:pet_detail', pet_id=pet.id)
    else:
        vaccine_form = VaccinationLogForm()

    if request.method == 'POST' and 'document_submit' in request.POST:
        document_form = PetDocumentForm(request.POST, request.FILES)
        if document_form.is_valid():
            doc = document_form.save(commit=False)
            doc.pet = pet
            doc.save()
            return redirect('pets:pet_detail', pet_id=pet.id)
    else:
        document_form = PetDocumentForm()

    weight_logs = pet.weight_logs.order_by('-date')
    photos = pet.images.order_by('-uploaded_at')
    vaccinations = pet.vaccination_logs.order_by('-date_administered')
    tasks = pet.tasks.order_by('due_date')
    documents = pet.documents.all()  # с учётом ordering в модели PetDocument

    return render(request, 'pets/pet_detail.html', {
        'pet': pet,
        'weight_form': weight_form,
        'photo_form': photo_form,
        'vaccine_form': vaccine_form,
        'document_form': document_form,
        'weight_logs': weight_logs,
        'photos': photos,
        'vaccinations': vaccinations,
        'tasks': tasks,
        'documents': documents,
    })


@login_required
def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user  # <-- ВАЖНО
            pet.save()
            return redirect('pets:pet_detail', pet_id=pet.id)
    else:
        form = PetForm()
    return render(request, 'pets/pet_form.html', {'form': form})


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
    return render(request, 'pets/pet_form.html', {'form': form, 'pet': pet})


@login_required
def pet_delete(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        pet.delete()
        return redirect('pets:pet_list')
    return render(request, 'pets/pet_confirm_delete.html', {'pet': pet})
