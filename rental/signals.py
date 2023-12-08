
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings
from rent_app.tasks import async_send_rental_email
from rental_api.models import Rental
from rental.settings import *

## rent oluşturulduktan sonra asenkron send email fonksiyonuma yönlendiriyorum gerekli parametreler ile birlikte.
## mail içeriğinde fotoğraf olduğu için mail gönderme işlemi yaklaşık 1.5 ile 2 saniye arasında vakit alıyor.
## bu süreyi kullanıcının beklememesi için asenkron bir fonksiyon yaptım.
@receiver(post_save, sender=Rental)
def send_email_after_creation(sender, instance, created, **kwargs):
    if created:
        async_send_rental_email(
            instance.iha.id, 
            instance.rental_date, 
            instance.return_date, 
            instance.user.email
        )