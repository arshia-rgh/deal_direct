from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from django.urls import reverse

from utils.email_verification_generator import (
    generate_email_verification_token,
    generate_uid,
)


@shared_task
def send_email_verification_link(user_id):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.get(id=user_id)
    token = generate_email_verification_token(user)
    uid = generate_uid(user)

    verification_link = f"{settings.BASE_URL}{reverse('accounts:verify_email', kwargs={'uidb64': uid, 'token': token})}"

    subject = "Verify your email address"
    message = f"Please click the link below to verify your email address:\n{verification_link}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


@shared_task
def update_wallet_balance(user_id, amount):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.get(id=user_id)

    if user.is_active:
        User.objects.filter(id=user_id).update(wallet=F("wallet") + amount)


@shared_task
def send_password_reset_email(user_id):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    user = User.objects.get(id=user_id)

    token = generate_email_verification_token(user)
    uid = generate_uid(user)

    reset_link = f"{settings.BASE_URL}{reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

    subject = "Reset your password"
    message = f"Please click the link below to reset your password:\n{reset_link}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


@shared_task
def send_account_activity_report(user_id):
    pass
