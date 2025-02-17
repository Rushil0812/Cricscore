from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def detailed_timesince(value):
    if not value:
        return ""
    
    now = timezone.now()
    diff = now - value
    total_seconds = int(diff.total_seconds())
    
    if total_seconds < 60:
        return f"{total_seconds} seconds ago"
    
    minutes, seconds = divmod(total_seconds, 60)
    if minutes < 60:
        return f"{minutes} minutes {seconds} seconds ago"
    
    hours, minutes = divmod(minutes, 60)
    if hours < 24:
        return f"{hours} hours {minutes} minutes ago"
    
    days, hours = divmod(hours, 24)
    return f"{days} days {hours} hours ago"
    