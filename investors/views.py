from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from startups.models import InvestmentApplication, Startup
from .models import InvestorProfile
from accounts.models import User


def investor_login(request):
    """Login page for investors."""
    if request.user.is_authenticated:
        if request.user.is_investor():
            return redirect('investor_dashboard')
        return redirect('home')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_investor():
                login(request, user)
                return redirect('investor_dashboard')
            else:
                error = 'This account is not registered as an Investor.'
        else:
            error = 'Invalid username or password.'
    
    return render(request, 'investors/login.html', {'error': error})


def investor_register(request):
    """Registration page for investors."""
    if request.user.is_authenticated:
        if request.user.is_investor():
            return redirect('investor_dashboard')
        return redirect('home')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
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
                role='INVESTOR'
            )
            
            login(request, user)
            return redirect('investor_dashboard')
    
    return render(request, 'investors/register.html', {'error': error})


def investor_logout(request):
    """Logout for investors."""
    if request.method == 'POST':
        logout(request)
    return redirect('home')


@login_required(login_url='investor_login')
def investor_dashboard(request):
    """Dashboard for investors."""
    if not request.user.is_investor():
        return redirect('home')
    
    profile, created = InvestorProfile.objects.get_or_create(user=request.user)
    
    # Get recent startups
    startups = Startup.objects.filter(approved=True)[:6]
    
    # Get investment applications
    applications = InvestmentApplication.objects.filter(investor=profile).order_by('-created_at')[:5]
    
    return render(request, 'investors/dashboard.html', {
        'profile': profile,
        'startups': startups,
        'applications': applications,
    })


@login_required(login_url='investor_login')
def investor_profile(request):
    """Edit investor profile."""
    if not request.user.is_investor():
        return redirect('home')
    
    profile, created = InvestorProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.investment_range_min = request.POST.get('investment_range_min', 0) or 0
        profile.investment_range_max = request.POST.get('investment_range_max', 0) or 0
        profile.industry_focus = request.POST.get('industry_focus', '')
        profile.location = request.POST.get('location', '')
        profile.save()
        
        return redirect('investor_dashboard')
    
    return render(request, 'investors/profile.html', {'profile': profile})


@login_required(login_url='investor_login')
def browse_startups(request):
    """Browse all approved startups."""
    if not request.user.is_investor():
        return redirect('home')
    
    startups = Startup.objects.filter(approved=True)
    
    # Filter by niche
    niche = request.GET.get('niche')
    if niche:
        startups = startups.filter(niche__icontains=niche)
    
    # Filter by stage
    stage = request.GET.get('stage')
    if stage:
        startups = startups.filter(stage__icontains=stage)
    
    return render(request, 'investors/browse_startups.html', {'startups': startups})


@login_required(login_url='investor_login')
def startup_detail_investor(request, startup_id):
    """View startup details for investors."""
    if not request.user.is_investor():
        return redirect('home')
    
    startup = get_object_or_404(Startup, id=startup_id, approved=True)
    
    return render(request, 'investors/startup_detail.html', {'startup': startup})


@login_required(login_url='investor_login')
def investor_applications(request):
    if not request.user.is_investor():
        return redirect('home')

    applications = InvestmentApplication.objects.filter(
        investor__user=request.user
    ).order_by('-created_at')

    return render(request, 'investors/applications.html', {'applications': applications})


@login_required(login_url='investor_login')
def update_application_status(request, application_id, status):
    if not request.user.is_investor():
        return redirect('home')

    application = get_object_or_404(
        InvestmentApplication,
        id=application_id,
        investor__user=request.user
    )

    if status in ['ACCEPTED', 'REJECTED', 'MORE_INFO']:
        application.status = status
        application.save()

    return redirect('investor_applications')
