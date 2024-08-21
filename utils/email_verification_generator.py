from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def generate_email_verification_token(user):
    return default_token_generator.make_token(user)


def generate_uid(user):
    return urlsafe_base64_encode(force_bytes(user.pk))
