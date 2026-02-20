from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Q
from accounts.models import User, AdminProfile
from startups.models import Startup, InvestmentApplication
from manufacturers.models import ManufacturerProfile, ConnectionRequest
from investors.models import InvestorProfile


def admin_login(request):
    """Admin login page."""
    if request.user.is_authenticated and request.user.is_admin():
        return redirect('admin_dashboard')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_admin():
                login(request, user)
                return redirect('admin_dashboard')
            else:
                error = 'This account is not registered as an Admin.'
        else:
            error = 'Invalid username or password.'
    
    return render(request, 'admin_dashboard/login.html', {'error': error})


@login_required(login_url='admin_login')
def admin_dashboard(request):
    """Main admin dashboard with platform statistics."""
    if not request.user.is_admin():
        return redirect('home')
    
    # Get statistics
    total_users = User.objects.count()
    total_investors = User.objects.filter(role='INVESTOR').count()
    total_startups = User.objects.filter(role='STARTUP').count()
    total_manufacturers = User.objects.filter(role='MANUFACTURER').count()
    
    approved_startups = Startup.objects.filter(approved=True).count()
    pending_startups = Startup.objects.filter(approved=False).count()
    
    pending_applications = InvestmentApplication.objects.filter(status='PENDING').count()
    pending_connections = ConnectionRequest.objects.filter(status='PENDING').count()
    
    # Recent activity
    recent_startups = Startup.objects.all().order_by('-id')[:5]
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    recent_applications = InvestmentApplication.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_investors': total_investors,
        'total_startups': total_startups,
        'total_manufacturers': total_manufacturers,
        'approved_startups': approved_startups,
        'pending_startups': pending_startups,
        'pending_applications': pending_applications,
        'pending_connections': pending_connections,
        'recent_startups': recent_startups,
        'recent_users': recent_users,
        'recent_applications': recent_applications,
    }    
    return render(request, 'admin_dashboard/dashboard.html', context)


@login_required(login_url='admin_login')
def manage_startups(request):
    """View all startups and approve/reject them."""
    if not request.user.is_admin():
        return redirect('home')
    
    filter_type = request.GET.get('filter', 'all')
    search = request.GET.get('search', '')
    
    startups = Startup.objects.all()
    
    if filter_type == 'pending':
        startups = startups.filter(approved=False)
    elif filter_type == 'approved':
        startups = startups.filter(approved=True)
    
    if search:
        startups = startups.filter(Q(name__icontains=search) | Q(niche__icontains=search))
    
    startups = startups.order_by('-id')
    
    context = {
        'startups': startups,
        'filter_type': filter_type,
        'search': search,
    }
    
    return render(request, 'admin_dashboard/manage_startups.html', context)


@login_required(login_url='admin_login')
def startup_approval(request, startup_id, action):
    """Approve or reject a startup."""
    if not request.user.is_admin():
        return redirect('home')
    
    startup = get_object_or_404(Startup, id=startup_id)
    
    if action == 'approve':
        startup.approved = True
        messages.success(request, f'{startup.name} has been approved!')
    elif action == 'reject':
        startup.approved = False
        messages.info(request, f'{startup.name} has been rejected.')
    
    startup.save()
    return redirect('manage_startups')


@login_required(login_url='admin_login')
def manage_users(request):
    """View all users and manage them."""
    if not request.user.is_admin():
        return redirect('home')
    
    role_filter = request.GET.get('role', 'all')
    search = request.GET.get('search', '')
    
    users = User.objects.exclude(role='ADMIN')
    
    if role_filter != 'all':
        users = users.filter(role=role_filter)
    
    if search:
        users = users.filter(Q(username__icontains=search) | Q(email__icontains=search))
    
    users = users.order_by('-date_joined')
    
    context = {
        'users': users,
        'role_filter': role_filter,
        'search': search,
    }
    
    return render(request, 'admin_dashboard/manage_users.html', context)


@login_required(login_url='admin_login')
def user_detail(request, user_id):
    """View detailed information about a user."""
    if not request.user.is_admin():
        return redirect('home')
    
    user = get_object_or_404(User, id=user_id)
    
    if user.is_admin():
        return redirect('manage_users')
    
    context = {'user': user}
    
    if user.is_investor():
        profile = InvestorProfile.objects.filter(user=user).first()
        applications = InvestmentApplication.objects.filter(investor=profile).count()
        context['profile'] = profile
        context['applications'] = applications
    
    elif user.is_startup():
        startup = Startup.objects.filter(founder=user).first()
        applications = InvestmentApplication.objects.filter(startup=startup).count()
        connections = ConnectionRequest.objects.filter(startup=startup).count()
        context['startup'] = startup
        context['applications'] = applications
        context['connections'] = connections
    
    elif user.is_manufacturer():
        profile = ManufacturerProfile.objects.filter(user=user).first()
        connections = ConnectionRequest.objects.filter(manufacturer=profile).count()
        context['profile'] = profile
        context['connections'] = connections
    
    return render(request, 'admin_dashboard/user_detail.html', context)


@login_required(login_url='admin_login')
def manage_applications(request):
    """View all investment applications."""
    if not request.user.is_admin():
        return redirect('home')
    
    status_filter = request.GET.get('status', 'all')
    search = request.GET.get('search', '')
    
    applications = InvestmentApplication.objects.all()
    
    if status_filter != 'all':
        applications = applications.filter(status=status_filter)
    
    if search:
        applications = applications.filter(Q(startup__name__icontains=search) | Q(investor__user__username__icontains=search))
    
    applications = applications.order_by('-created_at')
    
    context = {
        'applications': applications,
        'status_filter': status_filter,
        'search': search,
    }
    
    return render(request, 'admin_dashboard/manage_applications.html', context)


@login_required(login_url='admin_login')
def manage_connections(request):
    """View all manufacturer-startup connection requests."""
    if not request.user.is_admin():
        return redirect('home')
    
    status_filter = request.GET.get('status', 'all')
    search = request.GET.get('search', '')
    
    connections = ConnectionRequest.objects.all()
    
    if status_filter != 'all':
        connections = connections.filter(status=status_filter)
    
    if search:
        connections = connections.filter(Q(startup__name__icontains=search) | Q(manufacturer__company_name__icontains=search))
    
    connections = connections.order_by('-created_at')
    
    context = {
        'connections': connections,
        'status_filter': status_filter,
        'search': search,
    }
    
    return render(request, 'admin_dashboard/manage_connections.html', context)


@login_required(login_url='admin_login')
def admin_logout(request):
    """Logout for admin."""
    if request.method == 'POST':
        logout(request)
    return redirect('home')


@login_required(login_url='admin_login')
def delete_user(request, user_id):
    """Delete a user account."""
    if not request.user.is_admin():
        return redirect('home')
    
    user = get_object_or_404(User, id=user_id)
    
    if user.role == 'ADMIN':
        messages.error(request, 'Cannot delete admin accounts.')
        return redirect('manage_users')
    
    username = user.username
    user.delete()
    messages.success(request, f'User {username} has been deleted.')
    
    return redirect('manage_users')
