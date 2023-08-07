from django.shortcuts import render, redirect
from .models import Event, Category
from django.http import HttpResponse
from datetime import datetime
import stripe
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
import json
from .helpers import send_email_user


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
            discount = float(request.POST['discount']) if request.POST['discount'] else 0
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

    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            event_id = data.get('event_id')
            if event_id:
                event_obj = Event.objects.get(pk=event_id)
                organizer = request.user.organizer
                event_obj.organizer = organizer

                for attribute in ['title', 'description', 'start_date', 'end_date', 'location', 'capacity']:
                    value = data.get(attribute)
                    if value is not None:
                        setattr(event_obj, attribute, value)

                is_paid_event = data.get('is_paid_event', False)
                if is_paid_event:
                    event_obj.is_paid_event = is_paid_event
                    event_obj.discount = data.get('discount', 0)
                    event_obj.price = data.get('price', 0)

                event_obj.is_published = data.get('is_published', False)
                event_obj.save()

                return JsonResponse({'message': 'Event updated successfully.'}, status=200)
            else:
                return JsonResponse({'message': 'Invalid event_id.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data.'}, status=400)
        except Event.DoesNotExist:
            return JsonResponse({'message': 'Event does not exist.'}, status=404)
    else:
        return render(request, 'create_event.html')


def created_events(request):
    events = Event.objects.filter(organizer=request.user.organizer)
    context = {'events': events}
    return render(request, 'created_events.html', context)


def event_page(request):
    # Get all published events
    published_events = Event.objects.filter(is_published=True)

    # Get all categories
    categories = Category.objects.all()

    categories_with_events = Category.objects.filter(events__is_published=True).distinct()

    context = {
        'published_events': published_events,
        'categories': categories,
        'categories_with_events': categories_with_events
    }

    return render(request, 'events.html', context)


def payment_success(request):
    event_id = request.GET.get('event_id')
    event_obj = Event.objects.get(id=event_id)
    user = request.user
    event_obj.attendees.add(user)
    subject = f"{event_obj.title} Registerd Successfully"
    reciver_mail = user.email
    body = f"""
            <p>Hello {user.first_name}</p>
            <p>      Event Date&Time:{event_obj.start_date} </p> 
        """
    send_email_user(reciver_mail, subject, body)
    return HttpResponse("Payment Successfull")


def payment_failed(request):
    subject = f"Registerd Failed"
    reciver_mail = request.user.email
    body = f"""
                <p>Hello {request.user.first_name}</p>
                <p>      Payment Failed </p> 
            """
    send_email_user(reciver_mail, subject, body)
    return HttpResponse("Payment Failed")


def checkout_session(request):
    user = request.user
    stripe.api_key = settings.STRIPE_API_KEY
    event = request.GET.get('event', 'Default')
    amount = int(float(request.GET.get('amount')) * 100)
    product = stripe.Product.create(name=event)

    price = stripe.Price.create(
        product=product['id'],
        unit_amount=amount,
        currency='usd'
    )
    success_url = request.build_absolute_uri(reverse('payment_success'))
    cancel_url = request.build_absolute_uri(reverse('payment_failed'))
    session = stripe.checkout.Session.create(
        line_items=[{'price': price['id'], 'quantity':1}],
        payment_method_types=['card'],
        mode='payment',
        success_url=f"{success_url}?event_id={request.GET.get('id')}",
        cancel_url=cancel_url,
        )

    return redirect(session.url)
