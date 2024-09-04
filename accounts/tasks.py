from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

from products.models import Product
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
    context = {
        "user": user,
        "verification_link": verification_link,
    }

    html_message = render_to_string("emails/email_verification_html.html", context)
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=html_message,
    )


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
    context = {
        "user": user,
        "reset_link": reset_link,
    }

    html_message = render_to_string("emails/password_reset_html.html", context)
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=html_message,
    )


@shared_task
def send_account_activity_report(user_id):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    user = User.objects.get(user_id)

    seven_days_ago = timezone.now() - timezone.timedelta(days=7)
    products_uploaded = Product.objects.filter(uploaded_by=user).filter(
        created__gte=seven_days_ago
    )
    products_bought = Product.objects.filter(bought_by=user).filter(
        modified__gte=seven_days_ago
    )

    report_html = render_to_string(
        "emails/account_activity_report_html.html",
        {
            "user": user,
            "products_uploaded": products_uploaded,
            "products_bought": products_bought,
        },
    )

    report_text = strip_tags(report_html)

    send_mail(
        "Your Account Activity Report",
        report_text,
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=report_html,
    )
