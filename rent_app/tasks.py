import json
import random
from django.core.mail import EmailMessage
from rent_app.views import get_cached_iha
from rental_api.models import *
from datetime import date, datetime
from rental.settings import *
from celery import shared_task
from django.core.mail import send_mail
from django.db import transaction
import threading
from decimal import Decimal
from django.core.cache import cache

## bu fonksiyonum siteye kayıtlı her kullanıcıya listemizdeki iha'ları mail atıyor ve sitemize giriş yapmasını sağlıyoruz.

@shared_task
def iha_is_valid():
    users = User.objects.all()
    ihas = Iha.objects.all()
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

## async_send_rental_email'ten sonra çalışır.
## bu işlem düz bir mail atma işlemi django send mail methodunu kullanmak yerine EmailMessage kullandım çünkü iletimde fotoğraf olmasını istedim.
## send mail'de ileti içerisine fotoğraf koyamıyoruz.
## burada gerekli parametreleri kaydettikten sonra içerisine iha'nın fotoğrafını da ekledikten sonra email send ediyoruz.
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

## bu fonksiyonum asenkron bir mail atma fonksiyonudur.
## bu fonksiyonda mailimin içeriğini belirleyip send email fonksiyonuma yönlendiriyorum gerekli parametreler ile birlikte 
## gönderirken bu işlemin ayrı bir thread(iş parçası) ile iş yapmasını söylüyorum bu işlem asenkron çalışır ve kullanıcı bu işlemler esnasında bekletilmez.
def async_send_rental_email(iha_id, rental_date, return_date, email_to):
    product = Iha.objects.get(id=iha_id)
    subject = f"Kiralama İşlemi Başarılı"
    message = f"Merhaba, {product.brand} {product.model} aracını {rental_date} / {return_date} tarihleri için kiralamanız gerçekleşti."

    thread = threading.Thread(target=send_email, args=(product,subject, message, email_to))
    thread.start()



@shared_task
def apply_discount():
    # Rastgele bir Iha nesnesi seç
    iha = random.choice(Iha.objects.all())
    
    # İndirim miktarını hesapla (örneğin %10 indirim)
    discount_percentage = Decimal('10.0')
    original_price = iha.price_per_day
    discounted_price = original_price * (1 - discount_percentage / Decimal('100'))

    # İndirimli fiyatı uygula
    iha.price_per_day = discounted_price
    iha.save()
    data_to_cache = json.dumps({
        "original_price": str(original_price),
        "discounted_price": str(discounted_price),
        "valid_until": (datetime.now() + timedelta(seconds=30)).isoformat()
    })

    # JSON verisini Redis'e kaydet
    cache.set(f"discounted_iha{iha.id}", data_to_cache, timeout=30)
    get_cached_iha(iha.id)
    # Belirli bir süre sonra eski fiyatına döndürmek için zamanlanmış görevi başlat
    revert_discount.apply_async((iha.id, original_price), eta=timezone.now() + timedelta(seconds=30))

@shared_task
def revert_discount(iha_id, original_price):
    # İndirim süresi dolduktan sonra eski fiyatını geri yükle
    iha = Iha.objects.get(id=iha_id)
    iha.price_per_day = original_price
    iha.save()
    return "Fiyat eskiye çevrildi."