from django.shortcuts import render, redirect
from .models import Event
from django.http import HttpResponse
from datetime import datetime


def create_event(request):
    if request.method == 'POST':
        event_obj = Event()
        organizer = request.user.organizer
        title = request.POST['title']
        description = request.POST['description']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        location = request.POST['location']
        capacity = int(request.POST['capacity'])
        is_paid_event = 'is_paid_event' in request.POST
        is_published = 'is_published' in request.POST
        if is_paid_event:
            discount = float(request.POST['discount'])
            price = float(request.POST['price'])
            event_obj.is_paid_event = is_paid_event
            event_obj.discount = discount
            event_obj.price = price

        event_obj.organizer = organizer
        event_obj.title = title
        event_obj.description = description
        event_obj.start_date = datetime.astimezone(datetime.fromisoformat(start_date))
        event_obj.end_date = datetime.astimezone(datetime.fromisoformat(end_date))
        event_obj.location = location
        event_obj.capacity = capacity
        event_obj.is_published = is_published
        event_obj.save()
        return HttpResponse(f"Your {event_obj.title} Event created successfully.")

    else:
        # For GET requests, render the form HTML
        return render(request, 'create_event.html')
