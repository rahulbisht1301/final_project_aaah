from django.db import models
from django.conf import settings

class ManufacturerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    industry = models.CharField(max_length=200)
    production_capacity = models.IntegerField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username
