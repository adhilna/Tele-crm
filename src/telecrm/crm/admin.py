from django.contrib import admin
from .models import TaskAssign

# Register your models here.


@admin.register(TaskAssign)
class TaskAssignAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'assigned_to', 'due_date', 'updated_at')
    search_fields = ('task_name', 'assigned_to__username')
    list_filter = ('due_date', 'updated_at')
