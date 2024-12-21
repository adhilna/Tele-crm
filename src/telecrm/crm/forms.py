from django import forms
from .models import TaskAssign, CallLog
from datetime import timedelta


class TaskAssignForm(forms.ModelForm):
    class Meta:
        model = TaskAssign
        fields = ['task_name', 'description', 'file', 'assigned_to', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DurationWidget(forms.TextInput):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs.update({'placeholder': 'HH:MM:SS'})
        super().__init__(attrs)

    def format_value(self, value):
        if isinstance(value, timedelta):
            total_seconds = int(value.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return value


class CallLogForm(forms.ModelForm):
    call_duration = forms.DurationField(widget=DurationWidget())

    class Meta:
        model = CallLog
        fields = ['name', 'place', 'phone_number', 'call_type', 'call_outcome', 'call_date', 'call_duration', 'notes']
        widgets = {
            'call_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
