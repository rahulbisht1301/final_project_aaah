from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('INVESTOR', 'Investor'),
        ('STARTUP', 'Startup'),
        ('MANUFACTURER', 'Manufacturer'),
        ('ADMIN', 'Admin'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def is_investor(self):
        return self.role == 'INVESTOR'

    def is_startup(self):
        return self.role == 'STARTUP'

    def is_manufacturer(self):
        return self.role == 'MANUFACTURER'

    def is_admin(self):
        return self.role == 'ADMIN'


class Message(models.Model):
    """Direct messages between users."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}: {self.subject}"


class AdminProfile(models.Model):
    """Admin profile for platform administrators."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True, default='Platform Management')
    is_super_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} (Admin)"
