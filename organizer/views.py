from django.shortcuts import render, get_object_or_404
from organizer.models import Organizer
from django.urls import reverse


def organizer_dashboard(request):
    organizer = get_object_or_404(Organizer, user=request.user)
    create_event_url = reverse('create_event')
    return render(request, 'organizer_dashboard.html', {'organizer': organizer, 'create_event_url': create_event_url})
