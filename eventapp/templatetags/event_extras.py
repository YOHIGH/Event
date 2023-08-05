from django import template
register = template.Library()


@register.filter
def is_registered(event, user):
  return event.attendees.filter(pk=user.pk).exists()
