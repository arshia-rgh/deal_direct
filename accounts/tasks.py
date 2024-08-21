from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from utils.email_verification_generator import (
    generate_email_verification_token,
    generate_uid,
)


@shared_task
def send_email_verification_link(user_id):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.get(user_id)
    token = generate_email_verification_token(user)
    uid = generate_uid(user)

    verification_link = f"{settings.BASE_URL}{reverse('accounts:verify_email', kwargs={'uidb64': uid, 'token': token})}"

    subject = "Verify your email address"
    message = f"Please click the link below to verify your email address:\n{verification_link}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
