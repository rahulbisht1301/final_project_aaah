from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from startups.models import Startup
from .models import ManufacturerProfile, ConnectionRequest
from accounts.models import User


def manufacturer_login(request):
    """Login page for manufacturers."""
    if request.user.is_authenticated:
        if request.user.is_manufacturer():
            return redirect('manufacturer_dashboard')
        return redirect('home')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_manufacturer():
                login(request, user)
                return redirect('manufacturer_dashboard')
            else:
                error = 'This account is not registered as a Manufacturer.'
        else:
            error = 'Invalid username or password.'
    
    return render(request, 'manufacturers/login.html', {'error': error})


def manufacturer_register(request):
    """Registration page for manufacturers."""
    if request.user.is_authenticated:
        if request.user.is_manufacturer():
            return redirect('manufacturer_dashboard')
        return redirect('home')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        company_name = request.POST.get('company_name', '')
        
        if password != confirm_password:
            error = 'Passwords do not match.'
        elif User.objects.filter(username=username).exists():
            error = 'Username already exists.'
        elif User.objects.filter(email=email).exists():
            error = 'Email already registered.'
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='MANUFACTURER'
            )
            
            # Update manufacturer profile with company name
            try:
                profile = ManufacturerProfile.objects.get(user=user)
                profile.company_name = company_name
                profile.save()
            except ManufacturerProfile.DoesNotExist:
                ManufacturerProfile.objects.create(user=user, company_name=company_name)
            
            login(request, user)
            return redirect('manufacturer_dashboard')
    
    return render(request, 'manufacturers/register.html', {'error': error})


def manufacturer_logout(request):
    """Logout for manufacturers."""
    if request.method == 'POST':
        logout(request)
    return redirect('home')


@login_required(login_url='manufacturer_login')
def manufacturer_dashboard(request):
    """Dashboard for manufacturers showing overview and recent startups."""
    if not request.user.is_manufacturer():
        return redirect('home')
    
    # Get approved startups
    startups = Startup.objects.filter(approved=True)[:5]
    
    # Get manufacturer's connection requests
    try:
        manufacturer = ManufacturerProfile.objects.get(user=request.user)
        connection_requests = ConnectionRequest.objects.filter(manufacturer=manufacturer).order_by('-created_at')[:5]
    except ManufacturerProfile.DoesNotExist:
        connection_requests = []
    
    return render(request, 'manufacturers/dashboard.html', {
        'startups': startups,
        'connection_requests': connection_requests,
    })


@login_required(login_url='manufacturer_login')
def startup_list(request):
    """View all approved startups."""
    if not request.user.is_manufacturer():
        return redirect('home')
    
    startups = Startup.objects.filter(approved=True)
    
    # Filter by niche if provided
    niche = request.GET.get('niche')
    if niche:
        startups = startups.filter(niche__icontains=niche)
    
    # Filter by stage if provided
    stage = request.GET.get('stage')
    if stage:
        startups = startups.filter(stage__icontains=stage)
    
    return render(request, 'manufacturers/startup_list.html', {
        'startups': startups,
    })


@login_required(login_url='manufacturer_login')
def startup_detail(request, startup_id):
    """View detailed information about a startup."""
    if not request.user.is_manufacturer():
        return redirect('home')
    
    startup = get_object_or_404(Startup, id=startup_id, approved=True)
    
    # Check if already connected
    try:
        manufacturer = ManufacturerProfile.objects.get(user=request.user)
        existing_request = ConnectionRequest.objects.filter(
            manufacturer=manufacturer, 
            startup=startup
        ).first()
    except ManufacturerProfile.DoesNotExist:
        existing_request = None
    
    return render(request, 'manufacturers/startup_detail.html', {
        'startup': startup,
        'existing_request': existing_request,
    })


@login_required(login_url='manufacturer_login')
def connect_to_startup(request, startup_id):
    """Send a connection request to a startup."""
    if not request.user.is_manufacturer():
        return redirect('home')
    
    startup = get_object_or_404(Startup, id=startup_id, approved=True)
    manufacturer = get_object_or_404(ManufacturerProfile, user=request.user)
    
    if request.method == 'POST':
        message = request.POST.get('message', '')
        
        # Create connection request if doesn't exist
        ConnectionRequest.objects.get_or_create(
            manufacturer=manufacturer,
            startup=startup,
            defaults={'message': message}
        )
        
        return redirect('startup_detail', startup_id=startup_id)
    
    return render(request, 'manufacturers/connect.html', {
        'startup': startup,
    })


@login_required(login_url='manufacturer_login')
def manufacturer_profile(request):
    """Edit manufacturer profile."""
    if not request.user.is_manufacturer():
        return redirect('home')
    
    profile, created = ManufacturerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.company_name = request.POST.get('company_name', '')
        profile.industry = request.POST.get('industry', '')
        profile.production_capacity = request.POST.get('production_capacity', 0) or 0
        profile.location = request.POST.get('location', '')
        profile.email = request.POST.get('email', '')
        profile.phone = request.POST.get('phone', '')
        profile.save()
        
        return redirect('manufacturer_dashboard')
    
    return render(request, 'manufacturers/profile.html', {'profile': profile})


@login_required(login_url='manufacturer_login')
def connection_history(request):
    """View all connection requests."""
    if not request.user.is_manufacturer():
        return redirect('home')
    
    try:
        manufacturer = ManufacturerProfile.objects.get(user=request.user)
        connections = ConnectionRequest.objects.filter(manufacturer=manufacturer).order_by('-created_at')
    except ManufacturerProfile.DoesNotExist:
        connections = []
    
    return render(request, 'manufacturers/connections.html', {'connections': connections})
