from django.core.mail import EmailMessage
from rental_api.models import *
from datetime import date, datetime
from rental.settings import *
from celery import shared_task
from django.core.mail import send_mail
from django.db import transaction
import threading


@shared_task
def iha_is_valid():
    users = User.objects.all()
    ihas = Iha.objects.filter(is_active=True)

    if not ihas.exists():
        return "Aktif iha bulunamadı."

    # İHA bilgilerini bir listeye dönüştürme
    iha_list = [f"{iha.brand} marka {iha.model} model, günlük fiyat: {iha.price_per_day} TL" for iha in ihas]

    # İHA listesini string olarak birleştirme
    iha_string = "\n".join(iha_list)

    for user in users:
        subject = f'Sayın {user.first_name}, kiralık araçlarımız var!'
        body = f"Sizin için kiralık araçlarımız var:\n{iha_string}"

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=EMAIL_HOST_USER,
            to=[user.email]
        )

        # İHA fotoğraflarını e-postaya ekle
        for iha in ihas:
            if iha.photo:
                email.attach_file(iha.photo.path)

        # E-postayı gönder
        email.send(fail_silently=False)

    return "E-postalar gönderildi."


    
def send_email(product,subject, message, email_to):
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=EMAIL_HOST_USER,
        to=[email_to]
    )
    
    if product.photo:
                email.attach_file(product.photo.path)
    email.send(fail_silently=False)

def async_send_rental_email(iha_id, rental_date, return_date, email_to):
    product = Iha.objects.get(id=iha_id)
    subject = f"Kiralama İşlemi Başarılı"
    message = f"Merhaba, {product.brand} {product.model} aracını {rental_date} / {return_date} tarihleri için kiralamanız gerçekleşti."

    thread = threading.Thread(target=send_email, args=(product,subject, message, email_to))
    thread.start()