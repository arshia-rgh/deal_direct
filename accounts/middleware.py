from django.contrib.sessions.models import Session
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class SessionTrackingMiddleware(MiddlewareMixin):
    """
    Middleware to track the last activity time of authenticated users.

    This middleware updates the session data with the current timestamp
    whenever an authenticated user makes a request.

    Methods:
        process_request(request):
            Updates the session data with the current timestamp if the user is authenticated.
    """

    def process_request(self, request):
        """
        Updates the session data with the current timestamp if the user is authenticated.

        Args:
            request (HttpRequest): The HTTP request object.

        Raises:
            Session.DoesNotExist: If the session does not exist.
        """

        if request.user.is_authenticated:
            session_key = request.session.session_key
            session = Session.objects.get(session_key=session_key)

            session_data = session.get_decoded()

            session_data["last_activity"] = timezone.now().isoformat()

            session.session_data = Session.objects.encode(session_data)

            session.save()
