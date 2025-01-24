from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from pets.forms import VaccinationForm
from pets.models import Pet, Vaccination


@login_required
def create_vaccination(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = VaccinationForm(request.POST)
        if form.is_valid():
            vac = form.save(commit=False)
            vac.pet = pet
            vac.created_by = request.user
            vac.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=vaccinations")
    else:
        form = VaccinationForm()

    return render(request, 'pets/forms/vaccination_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Add Vaccination"),
    })


@login_required
def edit_vaccination(request, vacc_id):
    vac = get_object_or_404(Vaccination, id=vacc_id, deleted_at__isnull=True)
    pet = vac.pet

    if request.user != pet.owner and request.user != pet.caregiver:
        return HttpResponseForbidden("You are not allowed to edit vaccination logs for this pet.")

    if request.method == 'POST':
        form = VaccinationForm(request.POST, request.FILES, instance=vac)
        if form.is_valid():
            v = form.save(commit=False)
            v.mark_as_edited(request.user)
            v.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=vaccinations")
    else:
        form = VaccinationForm(instance=vac)

    return render(request, 'pets/forms/vaccination_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Edit Vaccination"),
        'vaccination': vac,
    })


@login_required
def delete_vaccination(request, vacc_id):
    vaccination_log = get_object_or_404(Vaccination, id=vacc_id, deleted_at__isnull=True)
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
