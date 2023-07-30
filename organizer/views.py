from django.shortcuts import render, get_object_or_404
from organizer.models import Organizer


def organizer_dashboard(request):
    user_id = request.user.id
    organizer = get_object_or_404(Organizer, user_id=user_id)

    return render(request, 'organizer_dashboard.html', {'organizer': organizer})
