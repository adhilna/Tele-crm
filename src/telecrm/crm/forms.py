from django import forms
from .models import TaskAssign


class TaskAssignForm(forms.ModelForm):
    class Meta:
        model = TaskAssign
        fields = ['task_name', 'description', 'file', 'assigned_to', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
