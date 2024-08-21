from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import send_email_verification_link

User = get_user_model()


@receiver(post_save, sender=User)
def user_post_save_send_mail(sender, instance, created, **kwargs):
    if created:
        send_email_verification_link.delay(instance.id)
