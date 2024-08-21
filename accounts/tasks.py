from celery import shared_task

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
