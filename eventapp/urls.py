from django.urls import path
from . import views

urlpatterns = [
    # Your other URL patterns...
    path('create-event/', views.create_event, name='create_event'),
    path('created-events/', views.created_events, name='created_events'),
    path('', views.event_page, name='events'),
]
