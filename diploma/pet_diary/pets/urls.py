from django.urls import path

import pets.views

app_name = 'pets'

urlpatterns = [
    # PET
    path('', pets.views.pet.pet_list, name='pet_list'),
    path('create/', pets.views.pet.create_pet, name='pet_create'),
    path('<int:pet_id>/', pets.views.pet.pet_detail, name='pet_detail'),
    path('<int:pet_id>/edit/', pets.views.pet.edit_pet, name='pet_update'),
    path('<int:pet_id>/delete/', pets.views.pet.delete_pet, name='pet_delete'),

    # TASK
    path('<int:pet_id>/tasks/create/', pets.views.task.create_task, name='task_create'),
    path('tasks/<int:task_id>/edit/', pets.views.task.edit_task, name='task_edit'),
    path('tasks/<int:task_id>/delete/', pets.views.task.delete_task, name='task_delete'),
    path('<int:pet_id>/tasks/bulk_status/', pets.views.task.bulk_update_task_status, name='task_bulk_status'),

    # WEIGHT LOG
    path('<int:pet_id>/weight/create/', pets.views.weight_record.create_weight_record, name='weight_create'),
    path('weight/<int:weight_id>/edit/', pets.views.weight_record.edit_weight_record, name='weight_edit'),
    path('weight/<int:weight_id>/delete/', pets.views.weight_record.delete_weight_record, name='weight_delete'),

    # PHOTOS
    path('<int:pet_id>/photos/upload/', pets.views.image.upload_pet_image, name='photo_upload'),
    path('<int:pet_id>/image/<int:image_id>/edit/', pets.views.image.edit_pet_image, name='edit_pet_image'),
    path('<int:pet_id>/image/<int:image_id>/delete/', pets.views.image.delete_pet_image, name='delete_pet_image'),
    path('protected-media/<int:pet_id>/<str:image_name>/', pets.views.image.download_pet_image, name='protected_media'),

    # VACCINATIONS
    path('<int:pet_id>/vaccinations/create/', pets.views.vaccination.create_vaccination, name='vaccination_create'),
    path('vaccinations/<int:vacc_id>/edit/', pets.views.vaccination.edit_vaccination, name='vaccination_edit'),
    path('vaccinations/<int:vacc_id>/delete/', pets.views.vaccination.delete_vaccination, name='vaccination_delete'),

    # DOCUMENTS
    path('<int:pet_id>/documents/upload/', pets.views.document.upload_document, name='document_upload'),
    path('documents/<int:doc_id>/edit/', pets.views.document.edit_document, name='document_edit'),
    path('pet/<int:pet_id>/document/<int:doc_id>/delete/', pets.views.document.delete_document, name='delete_pet_document'),
    path('protected-media/documents/<int:pet_id>/<str:doc_name>/', pets.views.document.download_document, name='protected_media_document'),
]
