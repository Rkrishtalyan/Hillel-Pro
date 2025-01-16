from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import timedelta


class Pet(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pets',
        verbose_name=_("Owner")
    )
    name = models.CharField(max_length=100, verbose_name=_("Pet Name"))
    species = models.CharField(max_length=100, verbose_name=_("Species"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("Birth Date"))
    breed = models.CharField(max_length=100, blank=True, verbose_name=_("Breed"))
    chip_number = models.CharField(max_length=50, blank=True, verbose_name=_("Chip Number"))
    avatar = models.ImageField(upload_to='pet_avatars/', null=True, blank=True, verbose_name=_("Avatar"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    confirmed_diagnoses = models.TextField(
        blank=True,
        verbose_name=_("Confirmed Diagnoses")
    )
    current_prescriptions = models.TextField(
        blank=True,
        verbose_name=_("Current Prescriptions")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Pet")
        verbose_name_plural = _("Pets")


class PetImage(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_("Pet")
    )
    image = models.ImageField(
        upload_to='pet_images/',
        verbose_name=_("Image")
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Uploaded at")
    )

    def __str__(self):
        return f"{self.pet.name} (id={self.id})"

    class Meta:
        verbose_name = _("Pet Image")
        verbose_name_plural = _("Pet Images")


class WeightLog(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='weight_logs',
        verbose_name=_("Pet")
    )
    date = models.DateField(verbose_name=_("Date"))
    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Weight (kg)")
    )

    def __str__(self):
        return f"{self.pet.name} - {self.date}: {self.weight_kg} kg"

    class Meta:
        verbose_name = _("Weight Log")
        verbose_name_plural = _("Weight Logs")


class VaccinationLog(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='vaccination_logs',
        verbose_name=_("Pet")
    )
    vaccine_name = models.CharField(
        max_length=200,
        verbose_name=_("Vaccine Name")
    )
    date_administered = models.DateField(
        verbose_name=_("Date Administered"),
        default=timezone.now
    )
    next_due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Next Due Date")
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )

    def __str__(self):
        return f"{self.pet.name} - {self.vaccine_name}"

    class Meta:
        verbose_name = _("Vaccination Log")
        verbose_name_plural = _("Vaccination Logs")


class PetDocument(models.Model):
    class DocumentType(models.TextChoices):
        ANALYSIS = 'analysis', _("Analysis Result")
        EXAMINATION = 'examination', _("Examination Result")
        CONCLUSION = 'conclusion', _("Doctor Conclusion")
        OTHER = 'other', _("Other")

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_("Pet")
    )
    doc_file = models.FileField(
        upload_to='pet_documents/',
        verbose_name=_("Document File")
    )
    doc_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
        verbose_name=_("Document Type")
    )
    doc_date = models.DateField(
        default=timezone.now,
        verbose_name=_("Document Date")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Uploaded at")
    )

    def __str__(self):
        return f"{self.get_doc_type_display()} ({self.pet.name})"

    class Meta:
        verbose_name = _("Pet Document")
        verbose_name_plural = _("Pet Documents")
        ordering = ['-doc_date', '-created_at']


class Task(models.Model):

    class TaskStatus(models.TextChoices):
        PLANNED = 'planned', _("Planned")
        OVERDUE = 'overdue', _("Overdue")
        DONE = 'done', _("Done")
        SKIPPED = 'skipped', _("Skipped")

    REMIND_BEFORE_CHOICES = [
        ('15_min', _("15 minutes")),
        ('1_hour', _("1 hour")),
        ('4_hours', _("4 hours")),
        ('12_hours', _("12 hours")),
        ('1_day', _("1 day")),
        ('3_days', _("3 days")),
        ('1_week', _("1 week")),
    ]

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_("Pet")
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_("Title")
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Due Date")
    )
    due_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name=_("Due Time")
    )
    remind_me = models.BooleanField(
        default=False,
        verbose_name=_("Remind Me")
    )
    remind_before = models.CharField(
        max_length=20,
        choices=REMIND_BEFORE_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Remind Before")
    )
    status = models.CharField(
        max_length=10,
        choices=TaskStatus.choices,
        default=TaskStatus.PLANNED,
        verbose_name=_("Status")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )

    # Recurring task field (for task creation only)
    recurring = models.BooleanField(
        default=False,
        verbose_name=_("Recurring?")
    )
    recurring_days = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Number of days to repeat")
    )

    def __str__(self):
        return f"{self.title} (pet={self.pet.name}, status={self.status})"

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
