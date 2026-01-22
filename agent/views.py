from datetime import timedelta
from django.conf import settings
from django.utils import timezone

from django.utils.dateparse import parse_datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

from life_admin.models import Task, Reminder
from life_admin.tasks import send_reminder_email
from .planner import plan_from_prompt


@api_view(["POST"])
def plan_day(request):
    """
    Agent endpoint:
    - Takes a prompt
    - Produces a structured plan
    - Executes the plan by creating tasks + reminders
    - Schedules reminder emails using Celery
    """
    prompt = (request.data.get("prompt") or "").strip()
    if not prompt:
        return Response({"error": "prompt is required"}, status=400)

    try:
        plan = plan_from_prompt(prompt)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    created = []
    for item in plan.get("tasks", []):
        title = (item.get("title") or "").strip()
        due_at_str = item.get("due_at")
        remind_before = int(item.get("remind_minutes_before") or 30)

        if not title or not due_at_str:
            # Skip invalid items rather than crashing the whole request
            continue

        due_at = parse_datetime(due_at_str)
        if due_at is None:
            continue

        task = Task.objects.create(title=title, due_at=due_at)

        if getattr(settings, "PLANPAL_DEMO_MODE", False):
            # Demo: trigger reminders quickly (60 seconds from now)
            remind_at = timezone.now() + timedelta(seconds=60)
        else:
            remind_at = due_at - timedelta(minutes=remind_before)

        reminder = Reminder.objects.create(task=task, remind_at=remind_at)

        # Schedule Celery job to run exactly at remind_at
        send_reminder_email.apply_async(args=[reminder.id], eta=remind_at)

        created.append(
            {
                "task_id": task.id,
                "title": task.title,
                "due_at": task.due_at,
                "remind_at": reminder.remind_at,
                "remind_minutes_before": remind_before,
            }
        )

    return Response({"plan": plan, "created": created})
