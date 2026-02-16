from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import InvestmentApplication, Startup
from investors.models import InvestorProfile
from manufacturers.models import ConnectionRequest
from accounts.models import User


def startup_login(request):
    """Login page for startups."""
    if request.user.is_authenticated:
        if request.user.is_startup():
            return redirect('startup_dashboard')
        return redirect('home')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_startup():
                login(request, user)
                return redirect('startup_dashboard')
            else:
                error = 'This account is not registered as a Startup.'
        else:
            error = 'Invalid username or password.'
    
    return render(request, 'startups/login.html', {'error': error})


def startup_register(request):
    """Registration page for startups."""
    if request.user.is_authenticated:
        if request.user.is_startup():
            return redirect('startup_dashboard')
        return redirect('home')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        startup_name = request.POST.get('startup_name', '')
        
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
                role='STARTUP'
            )
            
            # Update startup profile with name
            try:
                startup = Startup.objects.get(founder=user)
                startup.name = startup_name
                startup.save()
            except Startup.DoesNotExist:
                Startup.objects.create(founder=user, name=startup_name, niche='', valuation=0, stage='', vision='')
            
            login(request, user)
            messages.success(request, f'Welcome to VentureHub, {username}! Your startup account has been created.')
            return redirect('startup_dashboard')
    
    return render(request, 'startups/register.html', {'error': error})


def startup_logout(request):
    """Logout for startups."""
    if request.method == 'POST':
        logout(request)
    return redirect('home')


@login_required(login_url='startup_login')
def startup_dashboard(request):
    """Dashboard for startups."""
    if not request.user.is_startup():
        return redirect('home')
    
    try:
        startup = Startup.objects.get(founder=request.user)
    except Startup.DoesNotExist:
        startup = Startup.objects.create(founder=request.user, name='', niche='', valuation=0, stage='', vision='')
    
    # Get connection requests from manufacturers
    connection_requests = ConnectionRequest.objects.filter(startup=startup).order_by('-created_at')
    pending_connections = connection_requests.filter(status='PENDING').count()
    total_connections = connection_requests.count()
    
    # Get investment applications
    investment_apps = InvestmentApplication.objects.filter(startup=startup).order_by('-created_at')
    pending_apps = investment_apps.filter(status='PENDING').count()
    accepted_apps = investment_apps.filter(status='ACCEPTED').count()
    total_apps = investment_apps.count()
    
    return render(request, 'startups/dashboard.html', {
        'startup': startup,
        'connection_requests': connection_requests[:5],
        'investment_apps': investment_apps[:5],
        'pending_connections': pending_connections,
        'total_connections': total_connections,
        'pending_apps': pending_apps,
        'accepted_apps': accepted_apps,
        'total_apps': total_apps,
    })


@login_required(login_url='startup_login')
def startup_profile(request):
    """Edit startup profile."""
    if not request.user.is_startup():
        return redirect('home')
    
    startup, created = Startup.objects.get_or_create(
        founder=request.user,
        defaults={'name': '', 'niche': '', 'valuation': 0, 'stage': '', 'vision': ''}
    )
    
    if request.method == 'POST':
        startup.name = request.POST.get('name', '')
        startup.niche = request.POST.get('niche', '')
        startup.valuation = request.POST.get('valuation', 0) or 0
        startup.stage = request.POST.get('stage', '')
        startup.vision = request.POST.get('vision', '')
        startup.email = request.POST.get('email', '')
        startup.phone = request.POST.get('phone', '')
        startup.website = request.POST.get('website', '')
        startup.demo_video = request.POST.get('demo_video', '')
        startup.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('startup_dashboard')
    
    return render(request, 'startups/profile.html', {'startup': startup})


@login_required(login_url='startup_login')
def handle_connection_request(request, request_id, action):
    """Accept or reject connection requests from manufacturers."""
    if not request.user.is_startup():
        return redirect('home')
    
    startup = get_object_or_404(Startup, founder=request.user)
    conn_request = get_object_or_404(ConnectionRequest, id=request_id, startup=startup)
    
    if action == 'accept':
        conn_request.status = 'ACCEPTED'
        messages.success(request, f'Connection request from {conn_request.manufacturer.company_name} accepted!')
    elif action == 'reject':
        conn_request.status = 'REJECTED'
        messages.info(request, f'Connection request from {conn_request.manufacturer.company_name} rejected.')
    
    conn_request.save()
    return redirect('startup_dashboard')


@login_required(login_url='startup_login')
def apply_to_investor(request, investor_id):
    if not request.user.is_startup():
        return redirect('home')

    startup = get_object_or_404(Startup, founder=request.user)
    investor = get_object_or_404(InvestorProfile, id=investor_id)

    if request.method == 'POST':
        message = request.POST.get('message')
        amount = request.POST.get('amount')
        equity = request.POST.get('equity')

        InvestmentApplication.objects.create(
            startup=startup,
            investor=investor,
            message=message,
            amount_requested=amount,
            equity_offered=equity
        )
        
        messages.success(request, 'Investment application submitted successfully!')
        return redirect('startup_dashboard')

