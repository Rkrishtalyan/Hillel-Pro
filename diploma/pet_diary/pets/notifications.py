from django.core.mail import send_mail
from django.conf import settings

from pets.models import Task
from pets.utils import send_telegram_message


def _notify_owner_about_result(task, new_status):
    owner = task.pet.owner
    caregiver = task.pet.caregiver
    if not caregiver:
        return

    if new_status == Task.TaskStatus.DONE:
        status_text = "done"
    else:
        status_text = "skipped"

    message_text = (
        f"Your caretaker {caregiver.first_name or caregiver.email} "
        f"has marked the task '{task.title}' as {status_text}."
    )

    if owner.communication_method == 'telegram' and owner.telegram_id:
        send_telegram_message(owner, message_text)
    else:
        send_mail(
            subject="Your caretaker updated a task",
            message=message_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[owner.email],
        )
