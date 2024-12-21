from django.shortcuts import render, redirect
from .forms import TaskAssignForm
from django.contrib import messages
from .models import TaskAssign
from django.core.paginator import Paginator

# Create your views here.


def taskList(request):
    if request.user.role == 'team_leader' or request.user.role == 'staff':
        tasks = TaskAssign.objects.filter(assigned_to=request.user)
    else:
        tasks = TaskAssign.objects.none()

    paginator = Paginator(tasks, 10)  # Show 10 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'tasks': tasks, 'page_number': page_obj}
    return render(request, 'tasks.html', context)


def taskAssign(request):
    if request.method == 'POST':
        form = TaskAssignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task assigned successfully')
            return redirect('crm:admin_task_list')
        else:
            messages.error(request, 'Failed to assign task')
    else:
        form = TaskAssignForm()
    context = {'form': form}
    return render(request, 'task_assign.html', context)


def adminTaskList(request):
    if request.user.role == 'admin':
        tasks = TaskAssign.objects.all()
    else:
        tasks = TaskAssign.objects.none()
    context = {'tasks': tasks}
    return render(request, 'admin_task_list.html', context)


def callLogs(request):
    context = {}
    return render(request, 'call_logs.html', context)


def add_call_log(request):
    context = {}
    return render(request, 'add_call_log.html', context)


def reminders(request):
    context = {}
    return render(request, 'reminders.html', context)


def addReminder(request):
    context = {}
    return render(request, 'add_reminder.html', context)