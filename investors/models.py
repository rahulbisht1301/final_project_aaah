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


class FavoriteStartup(models.Model):
    """Saved/favorited startups by investors or manufacturers."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    startup = models.ForeignKey('startups.Startup', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'startup']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} saved {self.startup.name}"
