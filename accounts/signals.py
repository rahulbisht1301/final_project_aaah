from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from investors.models import InvestorProfile
from manufacturers.models import ManufacturerProfile
from startups.models import Startup

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'INVESTOR':
            InvestorProfile.objects.create(user=instance)
        elif instance.role == 'MANUFACTURER':
            ManufacturerProfile.objects.create(user=instance)
        elif instance.role == 'STARTUP':
            Startup.objects.create(founder=instance, name="", niche="", valuation=0, stage="", vision="")
