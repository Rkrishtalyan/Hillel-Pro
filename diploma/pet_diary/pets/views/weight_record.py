from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from pets.forms import WeightRecordForm
from pets.models import Pet, WeightRecord


@login_required
def create_weight_record(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = WeightRecordForm(request.POST)
        if form.is_valid():
            w = form.save(commit=False)
            w.pet = pet
            w.created_by = request.user
            w.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet_id])}?tab=weight")
    else:
        form = WeightRecordForm()

    return render(request, 'pets/forms/weight_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Add Weight"),
    })


@login_required
def edit_weight_record(request, weight_id):
    wl = get_object_or_404(WeightRecord, id=weight_id)
    pet = wl.pet

    if request.user != pet.owner and request.user != pet.caregiver:
        return HttpResponseForbidden("You are not allowed to edit weight logs for this pet.")

    if request.method == 'POST':
        form = WeightRecordForm(request.POST, instance=wl)
        if form.is_valid():
            w = form.save(commit=False)
            w.mark_as_edited(request.user)
            w.save()
            return redirect(f"{reverse('pets:pet_detail', args=[pet.id])}?tab=weight")
    else:
        form = WeightRecordForm(instance=wl)

    return render(request, 'pets/forms/weight_form.html', {
        'form': form,
        'pet': pet,
        'title': _("Edit Weight"),
        'weight_log': wl,
    })


@login_required
def delete_weight_record(request, weight_id):
    weight_log = get_object_or_404(WeightRecord, id=weight_id)
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
