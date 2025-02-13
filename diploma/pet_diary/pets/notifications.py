from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext as _

from pets.models import Task
from pets.utils import send_telegram_message
from accounts.models import CommunicationMethod


def _notify_owner_about_result(task, new_status):
    owner = task.pet.owner
    caregiver = task.pet.caregiver
    pet = task.pet
    if not caregiver:
        return

    if new_status == Task.TaskStatus.DONE:
        status_text = "done"
    else:
        status_text = "skipped"

    message_text = _(
        "{pet_name}'s caretaker {caretaker} has marked the task '{task_title}' as {status}."
    ).format(
        pet_name=pet.name,
        caretaker=caregiver.first_name or caregiver.email,
        task_title=task.title,
        status=status_text,
    )
    if owner.communication_method == CommunicationMethod.TELEGRAM and owner.telegram_id:
        send_telegram_message(owner, message_text)
    else:
        send_mail(
            subject=_("Your caretaker updated a task"),
            message=message_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[owner.email],
        )
