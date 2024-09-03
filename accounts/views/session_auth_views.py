from django.contrib.sessions.models import Session
from django.utils import timezone
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAuthenticatedAndActive
from utils.mixins import ThrottleMixin, LoggingMixin


class SessionListAPIView(ThrottleMixin, LoggingMixin, APIView):
    """
    API view to list active sessions for the authenticated user.

    This view retrieves all active sessions and filters them to include only
    those belonging to the authenticated user.

    Methods:
        get(request, *args, **kwargs):
            Retrieves and returns the list of active sessions for the authenticated user.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    def get(self, request, *args, **kwargs):
        """
        Retrieves and returns the list of active sessions for the authenticated user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A response object containing the list of active sessions.
        """

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


class SessionLogoutDestroyView(ThrottleMixin, LoggingMixin, generics.DestroyAPIView):
    """
    API view to log out a specific session for the authenticated user.

    This view deletes a session if it belongs to the authenticated user.

    Methods:
        delete(request, *args, **kwargs):
            Deletes the specified session if it belongs to the authenticated user.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    def delete(self, request, *args, **kwargs):
        """
        Deletes the specified session if it belongs to the authenticated user.

        Args:
            request (HttpRequest): The HTTP request object.
            kwargs (dict): Additional keyword arguments, including the session key.

        Returns:
            Response: A response object indicating the result of the delete operation.
        """

        session_key = kwargs.get("session_key")

        try:
            session = Session.objects.get(session_key=session_key)

            session_data = session.get_decoded()

            if session_data.get("_auth_user_id") == str(request.user.id):
                session.delete()

                return Response(
                    {"message": "Session logged out successfully"},
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    {"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN
                )

        except Session.DoesNotExist:
            return Response(
                {"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND
            )
