import mimetypes
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from pets.forms import PetDocumentForm
from pets.models import Pet, PetDocument


@login_required
def upload_document(request, pet_id):
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
def edit_document(request, doc_id):
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
def delete_document(request, pet_id, doc_id):
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
def download_document(request, pet_id, doc_name):
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
