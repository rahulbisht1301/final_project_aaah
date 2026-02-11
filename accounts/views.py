from django.shortcuts import redirect

def role_based_redirect(request):
    if request.user.role == 'INVESTOR':
        return redirect('investor_dashboard')
    elif request.user.role == 'STARTUP':
        return redirect('startup_dashboard')
    elif request.user.role == 'MANUFACTURER':
        return redirect('manufacturer_dashboard')
