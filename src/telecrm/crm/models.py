from django.db import models
from django.conf import settings

# Create your models here.


class TaskAssign(models.Model):
    TASK_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    task_name = models.CharField(max_length=128)
    description = models.TextField(max_length=256)
    file = models.FileField(upload_to='task_files/', null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Dynamically reference the user model
        on_delete=models.CASCADE
    )
    due_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=128, choices=TASK_STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.task_name


class CallLog(models.Model):
    CALL_TYPE_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ]
    CALL_OUTCOME_CHOICES = [
        ('rejected', 'Rejected'),
        ('missed', 'Missed'),
        ('completed', 'Completed'),
    ]
    name = models.CharField(max_length=128)
    place = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)
    call_type = models.CharField(max_length=10, choices=CALL_TYPE_CHOICES)
    call_outcome = models.CharField(max_length=10, choices=CALL_OUTCOME_CHOICES)
    call_date = models.DateTimeField()
    call_duration = models.DurationField()
    notes = models.TextField(blank=True, null=True)
    logged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='logged_calls',
        default=True
    )


    def __str__(self):
        return f'called on {self.call_date} to {self.name}'
