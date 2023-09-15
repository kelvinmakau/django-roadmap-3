# session_timeout/middleware.py
from django.contrib.auth import logout
from django.conf import settings
from django.utils import timezone
from django.contrib import messages

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)  # Process the response first

        # Check if the user is authenticated
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')

            # Check if the session has expired
            if last_activity and (timezone.now() - last_activity).seconds >= settings.SESSION_COOKIE_AGE:
                messages.error(request, 'Your session has timed out due to inactivity.')
                logout(request)
            else:
                request.session['last_activity'] = timezone.now()

        return response
