from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.paginator import Paginator
from startups.models import InvestmentApplication, Startup
from .models import InvestorProfile, FavoriteStartup
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
            messages.success(request, f'Welcome to VentureHub, {username}! Your investor account has been created.')
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
    total_startups = Startup.objects.filter(approved=True).count()
    
    # Get investment applications
    applications = InvestmentApplication.objects.filter(investor=profile).order_by('-created_at')
    total_applications = applications.count()
    pending_applications = applications.filter(status='PENDING').count()
    accepted_applications = applications.filter(status='ACCEPTED').count()
    
    return render(request, 'investors/dashboard.html', {
        'profile': profile,
        'startups': startups,
        'applications': applications[:5],
        'total_startups': total_startups,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'accepted_applications': accepted_applications,
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
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('investor_dashboard')
    
    return render(request, 'investors/profile.html', {'profile': profile})


@login_required(login_url='investor_login')
def browse_startups(request):
    """Browse all approved startups."""
    if not request.user.is_investor():
        return redirect('home')
    
    startups = Startup.objects.filter(approved=True)
    
    # Search
    search = request.GET.get('search')
    if search:
        startups = startups.filter(name__icontains=search)
    
    # Filter by niche
    niche = request.GET.get('niche')
    if niche:
        startups = startups.filter(niche__icontains=niche)
    
    # Filter by stage
    stage = request.GET.get('stage')
    if stage:
        startups = startups.filter(stage__icontains=stage)
    
    # Pagination
    paginator = Paginator(startups, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get user's favorite startup IDs
    favorite_ids = FavoriteStartup.objects.filter(user=request.user).values_list('startup_id', flat=True)
    
    return render(request, 'investors/browse_startups.html', {
        'startups': page_obj,
        'page_obj': page_obj,
        'favorite_ids': list(favorite_ids),
    })


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
        
        if status == 'ACCEPTED':
            messages.success(request, f'Application from {application.startup.name} accepted!')
        elif status == 'REJECTED':
            messages.info(request, f'Application from {application.startup.name} rejected.')
        else:
            messages.info(request, f'Requested more info from {application.startup.name}.')

    return redirect('investor_applications')


@login_required(login_url='investor_login')
def toggle_favorite(request, startup_id):
    """Add or remove a startup from favorites."""
    if not request.user.is_investor():
        return redirect('home')
    
    startup = get_object_or_404(Startup, id=startup_id, approved=True)
    favorite, created = FavoriteStartup.objects.get_or_create(
        user=request.user,
        startup=startup
    )
    
    if created:
        messages.success(request, f'{startup.name} added to favorites!')
    else:
        favorite.delete()
        messages.info(request, f'{startup.name} removed from favorites.')
    
    # Redirect back to where they came from
    next_url = request.GET.get('next', 'browse_startups')
    return redirect(next_url)


@login_required(login_url='investor_login')
def saved_startups(request):
    """View saved/favorite startups."""
    if not request.user.is_investor():
        return redirect('home')
    
    favorites = FavoriteStartup.objects.filter(user=request.user).select_related('startup')
    startups = [fav.startup for fav in favorites]
    
    return render(request, 'investors/saved_startups.html', {'startups': startups})
