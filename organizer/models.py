from django.db import models
from userapp.models import CustomUser
from ckeditor.fields import RichTextField


class Organizer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=100)
    description = RichTextField()
    logo = models.ImageField(upload_to='organizer_logos/', blank=True, null=True)
    address = models.TextField()
    organization_type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.organization_name
