# Iha Kiralama Case
[Proje Videosu](https://youtu.be/Ses6lbxb3UY)


## Kullanılan Teknolojiler 
- Python
  - Rest Framework
  - Django
  - Django Signal
- Account
  - Django-Allauth

- UI
  - Swagger

- Database
  - Postgresql
    
- REST
  - Jquery DataTable 
  - Ajax
  - JQuery
    
- Cache
   - Redis
     
- Cronjob
  - Celery



# Başlangıç


## 1. Docker oluşturma & Migrations & Superuser oluşturma

- Ana dizinde olmalısınız. `root`

```sh
docker-compose build
```

- Docker üzerinden Migration Yapmak.

```sh
docker-compose run django python manage.py migrate
```

-  Superuser Oluşturmak.

```sh
docker-compose run django python manage.py createsuperuser
```

- Docker Çalıştırmak.

```sh
docker-compose up
```

-Şu anda [127.0.0.1:8000](127.0.0.1:8000) Online'sınız 🚀
- Admin panel [127.0.0.1:8000/admin](127.0.0.1:8000/admin)
- İstediğinizi oluşturabilirsiniz!
# İşleyiş

 - Bu bir iha kiralama sayfasıdır.Bu sayfada kullanıcılar Admin tarafından eklenen İha'ları listeler.Kullanıcılar Listelenen İha'lar arasından kiralamak istediği iha'yı seçer ve kimsenin kiralamadığı tarihler arasından bir seçim yapar,eğer başka bir kullanıcı o tarihlerde kiralama işlemi yaptıysa o günler diğer kullanıcılar için inactive oluyor ve kiralama yapılamıyor.
   
 - #(Django-Singals) Kiralama işlemi yapıldıktan sonra Kiralanan tarihler ve kiralanan İha kullanıcıya Mail yoluyla bilgilendirme yapılır.
   - Normalde bu fonksiyonda iletilen bir fotoğraf olduğu için kayıt işleminde 1.5 saniye ile 2 saniye arasında bekletiliyor kullanıcılar fakat bu fonksiyon için bir Threds kullandım ve mail atılmaya çalışırken ve fotoğraf yüklenmeye çalışırken yeni bir threds'te işlemine devam ediyor ve kullanıcıları bu esnada bekletmeden diğer işleme geçiyor Mail de o sırada atılıyor.
   - ![kiralama_başarılı](https://github.com/mciray/iha_rental/assets/81428294/05c653c9-65c7-46e0-9049-d24c0c8fca7d)

 - #(Celery)Uzun süre giriş yapmayan Kullanıcılar için Siteye ziyaret etmeleri için hatırlatıcı bir mail atıyorum kullanıcıları siteye çekebilmek için.
   - ![inactive](https://github.com/mciray/iha_rental/assets/81428294/9a823b33-a843-4905-bbf2-bb50f572ce87)
  
 - (Celery) Burada bütün kullanıcılar için sitemizdeki ürünleri günlük fiyatları ve görüntüleri ile birlikte kullanıcılara iletiyorum.
    - ![ihalar](https://github.com/mciray/iha_rental/assets/81428294/d43c24b6-04d9-4553-901a-3cde10be9f43)




