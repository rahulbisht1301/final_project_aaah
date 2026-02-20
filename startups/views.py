from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.paginator import Paginator
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
def apply_to_investors(request, investor_id=None):
    """Allow a startup to pitch to one or more investors.

    If an `investor_id` is provided via URL, that investor will be pre‑selected
    in the form. Otherwise the form displays all investors and the startup may
    choose multiple entries.  Submitting the form creates a separate
    InvestmentApplication for each selected investor.
    """
    if not request.user.is_startup():
        return redirect('home')

    startup = get_object_or_404(Startup, founder=request.user)

    if request.method == 'POST':
        # try to pull a list of investor IDs (multiple selection) or single
        investor_ids = request.POST.getlist('investor_ids')
        if not investor_ids:
            # fallback for the single‑id POST; keep compatibility with old
            # endpoints or forms that sent a single field named investor_id
            single = request.POST.get('investor_id')
            if single:
                investor_ids = [single]

        subject = request.POST.get('subject', '')
        message = request.POST.get('message')
        amount = request.POST.get('amount')
        equity = request.POST.get('equity')

        created = 0
        for inv_id in investor_ids:
            try:
                investor = InvestorProfile.objects.get(id=inv_id)
            except InvestorProfile.DoesNotExist:
                continue

            InvestmentApplication.objects.create(
                startup=startup,
                investor=investor,
                subject=subject,
                message=message,
                amount_requested=amount,
                equity_offered=equity,
            )
            created += 1

        if created:
            messages.success(request, f"Investment application{'s' if created != 1 else ''} submitted successfully!")
        else:
            messages.error(request, 'No valid investor selected.')
        return redirect('startup_dashboard')

    # GET – render the form
    investors = InvestorProfile.objects.all().order_by('user__username')
    selected = None
    if investor_id:
        selected = InvestorProfile.objects.filter(id=investor_id).first()

    return render(request, 'startups/apply.html', {
        'investors': investors,
        'selected': selected,
    })


@login_required(login_url='startup_login')
def startup_applications_history(request):
    """View all investment applications sent by the startup with pagination."""
    if not request.user.is_startup():
        return redirect('home')

    startup = get_object_or_404(Startup, founder=request.user)
    applications = InvestmentApplication.objects.filter(startup=startup).order_by('-created_at')

    # Pagination
    paginator = Paginator(applications, 10)  # 10 applications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'startups/applications_history.html', {
        'page_obj': page_obj,
        'applications': page_obj,
    })


@login_required(login_url='startup_login')
def startup_application_detail(request, application_id):
    """View detailed information of a single investment application."""
    if not request.user.is_startup():
        return redirect('home')

    startup = get_object_or_404(Startup, founder=request.user)
    application = get_object_or_404(InvestmentApplication, id=application_id, startup=startup)

    return render(request, 'startups/application_detail.html', {
        'application': application,
    })


@login_required(login_url='startup_login')
def delete_application(request, application_id):
    """Delete an investment application (only if not ACCEPTED)."""
    if not request.user.is_startup():
        return redirect('home')

    startup = get_object_or_404(Startup, founder=request.user)
    application = get_object_or_404(InvestmentApplication, id=application_id, startup=startup)

    # Only allow deletion if application is still pending
    if application.status != 'PENDING':
        messages.error(request, 'Only pending applications can be deleted.')
        return redirect('startup_application_detail', application_id=application.id)

    application.delete()
    messages.success(request, 'Application deleted successfully.')
    return redirect('startup_applications_history')


@login_required(login_url='startup_login')
def startup_connection_history(request):
    """View all manufacturer connection requests for the startup with pagination."""
    if not request.user.is_startup():
        return redirect('home')

    startup = get_object_or_404(Startup, founder=request.user)
    connections = ConnectionRequest.objects.filter(startup=startup).order_by('-created_at')

    # Pagination
    paginator = Paginator(connections, 10)  # 10 connections per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'startups/connection_history.html', {
        'page_obj': page_obj,
        'connections': page_obj,
    })


@login_required(login_url='startup_login')
def startup_connection_detail(request, connection_id):
    """View detailed information about a single connection."""
    if not request.user.is_startup():
        return redirect('home')

    startup = get_object_or_404(Startup, founder=request.user)
    connection = get_object_or_404(ConnectionRequest, id=connection_id, startup=startup)

    return render(request, 'startups/connection_detail.html', {
        'connection': connection,
    })


@login_required(login_url='startup_login')
def unfriend_connection(request, connection_id):
    """Change an accepted connection status to rejected (unfriend)."""
    if not request.user.is_startup():
        return redirect('home')

    if request.method != 'POST':
        return redirect('startup_connection_history')

    startup = get_object_or_404(Startup, founder=request.user)
    connection = get_object_or_404(ConnectionRequest, id=connection_id, startup=startup)

    # Only allow unfriending if the connection is ACCEPTED
    if connection.status != 'ACCEPTED':
        messages.error(request, 'Only accepted connections can be unfriended.')
        return redirect('startup_connection_history')

    connection.status = 'REJECTED'
    connection.save()
    messages.success(request, f'Connection with {connection.manufacturer.company_name} removed.')
    return redirect('startup_connection_history')

