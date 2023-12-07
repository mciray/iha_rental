
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings
from rent_app.tasks import async_send_rental_email
from rental_api.models import Rental
from rental.settings import *


@receiver(post_save, sender=Rental)
def send_email_after_creation(sender, instance, created, **kwargs):
    if created:
        async_send_rental_email(
            instance.iha.id, 
            instance.rental_date, 
            instance.return_date, 
            instance.user.email
        )