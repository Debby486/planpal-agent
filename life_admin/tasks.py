from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Reminder


@shared_task
def send_reminder_email(reminder_id: int):
    reminder = Reminder.objects.select_related("task").get(id=reminder_id)

    # Prevent duplicate sends (idempotency)
    if reminder.sent_at:
        return "already_sent"

    task = reminder.task

    subject = f"PlanPal Reminder: {task.title}"
    body = (
        f"Task: {task.title}\n"
        f"Due at: {task.due_at}\n"
        f"Reminder time: {reminder.remind_at}\n"
    )

    # from_email=None -> uses DEFAULT_FROM_EMAIL
    send_mail(subject, body, None, ["you@demo.local"])

    reminder.sent_at = timezone.now()
    reminder.save(update_fields=["sent_at"])
    return "sent"
