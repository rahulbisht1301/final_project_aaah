from django.shortcuts import render

def investor_dashboard(request):
    return render(request, 'investors/dashboard.html')

from startups.models import InvestmentApplication
from django.contrib.auth.decorators import login_required

@login_required
def investor_applications(request):
    if not request.user.is_investor():
        return redirect('home')

    applications = InvestmentApplication.objects.filter(
        investor__user=request.user
    ).order_by('-created_at')

    return render(request, 'investors/applications.html', {'applications': applications})

@login_required
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
