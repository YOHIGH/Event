from django.db import models
from organizer.models import Organizer
from ckeditor.fields import RichTextField
from userapp.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='events', on_delete=models.CASCADE, null=True, blank=True)
    attendees = models.ManyToManyField(CustomUser, related_name='events_attending', blank=True)
    title = models.CharField(max_length=100)
    description = RichTextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.TextField()
    capacity = models.PositiveIntegerField()
    is_published = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_paid_event = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_expired = models.BooleanField(default=False, editable=False)
    image = models.ImageField(upload_to='event_logos/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.start_date.date() <= now.date() or self.end_date.date() <= now.date():
            raise ValueError("Start date and end date should be greater than today's date.")
        if self.end_date <= self.start_date:
            raise ValueError("End date should be greater than start date.")

        super().save(*args, **kwargs)

    def time_left_to_start(self):
        now = timezone.now()
        if self.start_date < now:
            return {
                'days': 0,
                'hours': 0,
                'minutes': 0,
                'seconds': 0
            }

        time_left = self.start_date - now

        days = max(int(time_left.total_seconds() // 86400), 0)
        hours = max(int((time_left.total_seconds() % 86400) // 3600), 0)
        minutes = max(int((time_left.total_seconds() % 3600) // 60), 0)
        seconds = max(int(time_left.total_seconds() % 60), 0)

        return {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        }

    def event_duration(self):
        now = timezone.now()
        if self.end_date < now:
            return {
                'days': 0,
                'hours': 0,
                'minutes': 0,
                'seconds': 0
            }

        duration = self.end_date - self.start_date

        days = max(int(duration.total_seconds() // 86400), 0)
        hours = max(int((duration.total_seconds() % 86400) // 3600), 0)
        minutes = max(int((duration.total_seconds() % 3600) // 60), 0)
        seconds = max(int(duration.total_seconds() % 60), 0)

        return {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        }

    def remaining_tickets(self):
        return self.capacity - self.attendees.count()

    def get_discounted_price(self):
        if self.discount > 0:
            discounted_price = self.price * (1 - self.discount / 100)
            return discounted_price
        else:
            return self.price

    def already_registerd(self, request):
        if request in Event.objects.get(id=self.id).attendees.all():
            return True
        else:
            return False
