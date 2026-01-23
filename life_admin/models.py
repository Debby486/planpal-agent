from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=255)
    due_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="todo")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Reminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="reminders")
    remind_at = models.DateTimeField()
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.task.title} at {self.remind_at}"
