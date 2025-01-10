from django.urls import path
from pets import views


app_name = 'pets'

urlpatterns = [
    path('', views.pet_list, name='pet_list'),
    path('create/', views.pet_create, name='pet_create'),
    path('<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('<int:pet_id>/edit/', views.pet_update, name='pet_update'),
    path('<int:pet_id>/delete/', views.pet_delete, name='pet_delete'),
]
