# signals.py

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def post_user_created(sender, instance, created, **kwargs):
    if created:
        # Send a welcome email to the new user
        subject = 'Welcome to Our Appointment Platform!'
        message = (
            f"Hi {instance.username},\n\n"
            "Thank you for registering at our platform. We're excited to have you on board!"
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
