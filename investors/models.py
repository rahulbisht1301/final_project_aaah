from django.db import models
from django.conf import settings

class InvestorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    investment_range_min = models.DecimalField(max_digits=12, decimal_places=2)
    investment_range_max = models.DecimalField(max_digits=12, decimal_places=2)
    industry_focus = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username
