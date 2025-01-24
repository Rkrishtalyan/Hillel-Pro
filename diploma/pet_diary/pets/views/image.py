import mimetypes
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from pets.forms import PetImageForm
from pets.models import Pet, PetImage


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
    return render(request, 'pets/forms/photo_form.html', context)


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
    return render(request, 'pets/forms/photo_form.html', context)


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
