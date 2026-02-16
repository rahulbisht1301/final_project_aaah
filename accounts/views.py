from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import User


@login_required
def role_based_redirect(request):
    if request.user.role == 'INVESTOR':
        return redirect('investor_applications')
    elif request.user.role == 'STARTUP':
        return redirect('home')  # Update when startup dashboard exists
    elif request.user.role == 'MANUFACTURER':
        return redirect('manufacturer_dashboard')
    return redirect('home')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {
                'error': 'Username already exists'
            })
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        
        login(request, user)
        return redirect('role_redirect')
    
    return render(request, 'registration/register.html')
