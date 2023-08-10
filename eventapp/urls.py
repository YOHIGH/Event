from django.urls import path
from . import views

urlpatterns = [
    # Your other URL patterns...
    path('create-event/', views.create_event, name='create_event'),
    path('created-events/', views.created_events, name='created_events'),
    path('', views.event_page, name='events'),
    path('create-checkout/', views.checkout_session, name='create_checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('toggle_interest/', views.toggle_interest, name='toggle_interest'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('interested/', views.interested_events, name='interested_events'),
]
