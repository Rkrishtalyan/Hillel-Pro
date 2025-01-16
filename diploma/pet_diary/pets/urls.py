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

    # PHOTOS
    path('<int:pet_id>/photos/upload/', views.photo_upload, name='photo_upload'),

    # VACCINATIONS
    path('<int:pet_id>/vaccinations/create/', views.vaccination_create, name='vaccination_create'),
    path('vaccinations/<int:vacc_id>/edit/', views.vaccination_edit, name='vaccination_edit'),

    # DOCUMENTS
    path('<int:pet_id>/documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<int:doc_id>/edit/', views.document_edit, name='document_edit'),
]
