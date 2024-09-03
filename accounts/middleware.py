from django.contrib.sessions.models import Session
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class SessionTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key
            session = Session.objects.get(sesssion_key=session_key)

            session_data = session.get_decoded()

            session_data["last_activity"] = timezone.now().isoformat()

            session.session_data = Session.objects.encode(session_data)

            session.save()
