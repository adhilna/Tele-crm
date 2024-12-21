from django.db import models
from django.conf import settings

# Create your models here.


class TaskAssign(models.Model):
    task_name = models.CharField(max_length=128)
    description = models.TextField(max_length=256)
    file = models.FileField(upload_to='task_files/', null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Dynamically reference the user model
        on_delete=models.CASCADE
    )
    due_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name