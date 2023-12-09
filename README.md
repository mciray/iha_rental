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

![kiralama_başarılı](https://github.com/mciray/iha_rental/assets/81428294/05c653c9-65c7-46e0-9049-d24c0c8fca7d)
![inactive](https://github.com/mciray/iha_rental/assets/81428294/9a823b33-a843-4905-bbf2-bb50f572ce87)
![ihalar](https://github.com/mciray/iha_rental/assets/81428294/d43c24b6-04d9-4553-901a-3cde10be9f43)




