from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('task_list/', views.taskList, name='task_list'),
    path('task_assign/', views.taskAssign, name='task_assign'),
    path('call_logs/', views.callLogs, name='call_logs'),
    path('add_call_log/', views.add_call_log, name='add_call_log'),
    path('admin_task_list/', views.adminTaskList, name='admin_task_list'),
    # path('reminders/', views.reminders, name='reminders'),
    # path('add_reminder/', views.addReminder, name='add_reminder'),
]
