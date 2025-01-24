from django.contrib import admin
from pets.models import (
    Pet, PetImage, WeightRecord,
    Vaccination, Task, PetDocument
)


class PetDocumentInline(admin.TabularInline):
    model = PetDocument
    extra = 0
    fields = ('doc_type', 'doc_file', 'doc_date', 'description', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-doc_date', '-created_at')


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'species', 'breed')
    search_fields = ('name', 'breed', 'chip_number', 'species')
    inlines = [PetDocumentInline]


@admin.register(PetImage)
class PetImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'pet', 'uploaded_at')


@admin.register(WeightRecord)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'pet', 'date', 'weight_kg')
    list_filter = ('pet', 'date')


@admin.register(Vaccination)
class VaccinationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'pet', 'vaccine_name', 'date_administered', 'next_due_date')
    list_filter = ('pet', 'vaccine_name', 'date_administered', 'next_due_date')
    search_fields = ('vaccine_name', 'pet__name')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'pet', 'title', 'due_datetime', 'status')
    list_filter = ('pet', 'due_datetime', 'status')
    search_fields = ('title', 'pet__name')
