from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)

    # Additional fields for Event Registration user
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    # New fields for country, city, and state
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Check if the user's photo field is not set and gender is available
        if not self.photo and self.gender:
            # Set the default photo based on the user's gender
            if self.gender == self.MALE:
                self.photo = 'default_male.png'
            elif self.gender == self.FEMALE:
                self.photo = 'default_female.png'
            else:
                self.photo = 'default_other.png'
        elif not self.gender:
            self.photo = 'default_other.png'
        super().save(*args, **kwargs)
