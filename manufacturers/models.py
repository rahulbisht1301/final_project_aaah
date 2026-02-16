from django.db import models
from django.conf import settings
from django.utils import timezone


class ManufacturerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=200, blank=True, default='')
    production_capacity = models.IntegerField(default=0)
    location = models.CharField(max_length=200, blank=True, default='')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class ConnectionRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )
    
    manufacturer = models.ForeignKey(ManufacturerProfile, on_delete=models.CASCADE, related_name='connection_requests')
    startup = models.ForeignKey('startups.Startup', on_delete=models.CASCADE, related_name='manufacturer_requests')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('manufacturer', 'startup')
    
    def __str__(self):
        return f"{self.manufacturer.user.username} -> {self.startup.name}"

