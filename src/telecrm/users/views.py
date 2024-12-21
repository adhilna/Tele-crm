from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    # Add your dashboard logic here
    context = {}
    return render(request, 'dashboard.html', context)