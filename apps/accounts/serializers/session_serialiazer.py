from rest_framework import serializers


class SessionSerializer(serializers.Serializer):
    session_key = serializers.CharField(max_length=40)
    expire_date = serializers.DateTimeField()
    last_activity = serializers.DateTimeField(allow_null=True)
