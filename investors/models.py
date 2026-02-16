from django.db import models
from django.conf import settings

class InvestorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    investment_range_min = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    investment_range_max = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    industry_focus = models.CharField(max_length=200, blank=True, default='')
    location = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return self.user.username
