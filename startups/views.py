from django.shortcuts import get_object_or_404, redirect
from .models import InvestmentApplication, Startup
from investors.models import InvestorProfile
from django.contrib.auth.decorators import login_required

@login_required
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

        return redirect('startup_dashboard')
