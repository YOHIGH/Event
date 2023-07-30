from django.urls import path
from . import views

urlpatterns = [
    # Your other URL patterns...
    path('organizer/dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
]
