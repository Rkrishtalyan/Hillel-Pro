from django.urls import path
from pets import views

app_name = 'pets'

urlpatterns = [
    # PET
    path('', views.pet_list, name='pet_list'),
    path('create/', views.pet_create, name='pet_create'),
    path('<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('<int:pet_id>/edit/', views.pet_update, name='pet_update'),
    path('<int:pet_id>/delete/', views.pet_delete, name='pet_delete'),

    # TASK
    path('<int:pet_id>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('<int:pet_id>/tasks/bulk_status/', views.task_bulk_status, name='task_bulk_status'),

    # WEIGHT
    path('<int:pet_id>/weight/create/', views.weight_create, name='weight_create'),
    path('weight/<int:weight_id>/edit/', views.weight_edit, name='weight_edit'),
    path('weight/<int:weight_id>/delete/', views.weight_delete, name='weight_delete'),

    # PHOTOS
    path('<int:pet_id>/photos/upload/', views.photo_upload, name='photo_upload'),
    path('<int:pet_id>/image/<int:image_id>/edit/', views.edit_pet_image, name='edit_pet_image'),
    path('<int:pet_id>/image/<int:image_id>/delete/', views.delete_pet_image, name='delete_pet_image'),
    path('protected-media/<int:pet_id>/<str:image_name>/', views.protected_media, name='protected_media'),

    # VACCINATIONS
    path('<int:pet_id>/vaccinations/create/', views.vaccination_create, name='vaccination_create'),
    path('vaccinations/<int:vacc_id>/edit/', views.vaccination_edit, name='vaccination_edit'),
    path('vaccinations/<int:vacc_id>/delete/', views.vaccination_delete, name='vaccination_delete'),

    # DOCUMENTS
    path('<int:pet_id>/documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<int:doc_id>/edit/', views.document_edit, name='document_edit'),
    path('pet/<int:pet_id>/document/<int:doc_id>/delete/', views.delete_pet_document, name='delete_pet_document'),
    path('protected-media/documents/<int:pet_id>/<str:doc_name>/', views.protected_media_document, name='protected_media_document'),
]
