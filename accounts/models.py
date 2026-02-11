from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('INVESTOR', 'Investor'),
        ('STARTUP', 'Startup'),
        ('MANUFACTURER', 'Manufacturer'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def is_investor(self):
        return self.role == 'INVESTOR'

    def is_startup(self):
        return self.role == 'STARTUP'

    def is_manufacturer(self):
        return self.role == 'MANUFACTURER'
