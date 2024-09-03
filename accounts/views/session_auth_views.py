from django.contrib.sessions.models import Session
from django.utils import timezone
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAuthenticatedAndActive


class SessionListAPIView(APIView):
    permission_classes = (IsAuthenticatedAndActive,)

    def get(self, request, *args, **kwargs):
        sessions = Session.objects.filter(expire_date__gt=timezone.now())
        session_data = []

        for session in sessions:
            data = session.get_decoded()

            if data.get("_auth_user_id") == str(request.user.id):
                session_data.append(
                    {
                        "session_key": session.session_key,
                        "expire_date": session.expire_date,
                        "last_activity": data.get("last_activity"),
                    }
                )

        return Response(session_data, status=status.HTTP_200_OK)


class SessionLogoutDestroyView(generics.DestroyAPIView):
    pass
