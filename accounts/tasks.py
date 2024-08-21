from celery import shared_task


@shared_task
def send_email_verification_link(user_id):
    pass
