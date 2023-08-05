import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from eventapp.models import Event

logger = logging.getLogger('root')


class Command(BaseCommand):
    help = 'Check and update the is_expired field for all events'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_events = Event.objects.filter(end_date__lt=now)
        for event in expired_events:
            event.is_expired = True
            event.is_published = False
            event.save()
            self.log_expired_event(event, now)
        self.stdout.write(self.style.SUCCESS('Successfully updated is_expired for expired events.'))

    def log_expired_event(self, event, now):
        logger.info(f"Event '{event.title}' (ID: {event.pk}) has expired. End Date: {event.end_date}, Current Date: {now}.")
