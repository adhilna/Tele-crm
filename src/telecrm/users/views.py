from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from crm.models import TaskAssign, CallLog
from .models import User
from django.urls import reverse

# Create your views here.


from django.urls import reverse
from django.shortcuts import redirect


def registerView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            login(request, user)
            # Correctly using reverse with namespacing
            return redirect(reverse('users:login') + f'?username={user.username}')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()  # Strip whitespace
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Both username and password are required')
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('users:dashboard')  # Replace with your dashboard URL name
            else:
                messages.error(request, 'Invalid username or password')

    context = {'username': request.GET.get('username', '')}  # Pre-fill username if passed via GET
    return render(request, 'login.html', context)


def logoutView(request):
    logout(request)
    return redirect('users:login')


@login_required(login_url='login')
def dashboardView(request):
    if request.user.role == 'admin':
        tasks = TaskAssign.objects.all()
        call_logs = CallLog.objects.all()
        completed_tasks = tasks.filter(status='completed').count()
        total_tasks = tasks.count()
        completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks else 0
        context = {
            'tasks': tasks,
            'call_logs': call_logs,
            'completion_rate': round(completion_rate, 2),
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
        }

    elif request.user.role == 'team_leader':
        # Ensure that the team members' tasks are being fetched dynamically
        tasks = TaskAssign.objects.filter(assigned_to=request.user.id)
        print("Tasks for team:", tasks)
        call_logs = CallLog.objects.filter(logged_by=request.user.id)
        print("Call logs for team:", call_logs)
        completed_tasks = tasks.filter(status='completed').count()
        total_tasks = tasks.count()
        completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks else 0
        context = {
            'tasks': tasks,
            'call_logs': call_logs,
            'completion_rate': round(completion_rate, 2),
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
        }

    else:
        tasks = TaskAssign.objects.filter(assigned_to=request.user)
        call_logs = CallLog.objects.filter(logged_by=request.user)
        completed_tasks = tasks.filter(status='completed').count()
        total_tasks = tasks.count()
        completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks else 0
        context = {
            'tasks': tasks,
            'call_logs': call_logs,
            'completion_rate': round(completion_rate, 2),
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
        }

    return render(request, 'dashboard.html', context)

