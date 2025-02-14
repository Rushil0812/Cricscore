import pytz
from django.utils import timezone

class UserTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        tzname = request.session.get('django_timezone') or request.COOKIES.get('user_timezone')
        
        if tzname:
            try:
                timezone.activate(pytz.timezone(tzname))
            except Exception:
                timezone.deactivate()
        else:
            timezone.deactivate()
        
        response = self.get_response(request)
        return response