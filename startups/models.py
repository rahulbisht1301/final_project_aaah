from django.db import models
from django.conf import settings

class Startup(models.Model):
    founder = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    niche = models.CharField(max_length=200)
    valuation = models.DecimalField(max_digits=15, decimal_places=2)
    stage = models.CharField(max_length=100)
    vision = models.TextField()
    pitch_deck = models.FileField(upload_to='pitch_decks/')
    demo_video = models.URLField(blank=True)

    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

from django.utils import timezone

class InvestmentApplication(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('MORE_INFO', 'More Info Requested'),
    )

    startup = models.ForeignKey('Startup', on_delete=models.CASCADE, related_name='applications')
    investor = models.ForeignKey('investors.InvestorProfile', on_delete=models.CASCADE, related_name='applications')

    message = models.TextField()
    amount_requested = models.DecimalField(max_digits=15, decimal_places=2)
    equity_offered = models.DecimalField(max_digits=5, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.startup.name} -> {self.investor.user.username}"
