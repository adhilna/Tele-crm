from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskAssignForm, CallLogForm
from django.contrib import messages
from .models import TaskAssign, CallLog
from django.core.paginator import Paginator

# Create your views here.


def taskList(request):
    if request.user.role == 'team_leader' or request.user.role == 'staff':
        tasks = TaskAssign.objects.filter(assigned_to=request.user)
        if request.method == 'POST':
            task_id = request.POST.get('task_id')
            new_status = request.POST.get('status')
            task = get_object_or_404(TaskAssign, id=task_id)
            # Check if the task is assigned to the current user (staff or team leader)
            if task.assigned_to == request.user:
                task.status = new_status
                task.save()
                messages.success(request, f'Task status updated to {new_status.capitalize()}')
            else:
                messages.error(request, 'You cannot update this task status.')
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
    if request.user.role == 'admin':
        call_logs = CallLog.objects.all()
    else:
        call_logs = CallLog.objects.filter(logged_by=request.user)
    context = {'call_logs': call_logs}
    return render(request, 'call_logs.html', context)


def add_call_log(request):
    if request.method == 'POST':
        form = CallLogForm(request.POST)
        if form.is_valid():
            call_log = form.save(commit=False)
            call_log.logged_by = request.user  # Assign the logged-in user here
            call_log.save()
            messages.success(request, 'Call logged successfully')
            return redirect('crm:call_logs')
        else:
            print(form.errors)
            messages.error(request, 'Failed to log call')
    else:
        form = CallLogForm()
    context = {'form': form}
    return render(request, 'add_call_log.html', context)


def userPerformance(request):
    tasks = TaskAssign.objects.filter(assigned_to=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    completion_rate = (completed_tasks/total_tasks)*100 if total_tasks else 0

    context = {'total_tasks': total_tasks, 'completed_tasks': completed_tasks, 'completion_rate': completion_rate}
    return render(request, 'user_performance.html', context)


def userCallPerformance(request):
    calls = CallLog.objects.filter(logged_by=request.user)
    total_calls = calls.count()
    completed_calls = calls.filter(call_outcome='completed').count()
    missed_calls = calls.filter(call_outcome='missed').count()
    rejected_calls = calls.filter(call_outcome='rejected').count()

    context = {'total_calls': total_calls,
               'completed_calls': completed_calls,
               'missed_calls': missed_calls,
               'rejected_calls': rejected_calls
    }
    return render(request, 'call_performance.html', context)


# def adminDashboard(request):



def reminders(request):
    context = {}
    return render(request, 'reminders.html', context)


def addReminder(request):
    context = {}
    return render(request, 'add_reminder.html', context)