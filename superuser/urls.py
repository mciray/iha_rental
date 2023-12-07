from django.urls import path,include,re_path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
router = DefaultRouter()




urlpatterns = [
    path('',index,name="home"),
    path('create/iha/',create_iha,name="create_iha"),
    path('list_contact/',list_contact_admin,name="admin_contact_list"),
    path('index/graph/',user_activity_data,name="user_activity_data"),    
    path('iha/update/<int:id>/',iha_update_superuser,name="admin_iha_update"),
    path('admin/rental/update/<int:id>/',admin_rental_update,name="admin_rental_update"),
    path('list_ihas/',list_ihas_admin,name="admin_ihas_list"),
    path('list_rentals/',list_rentals_admin,name="admin_rental_list"),

    
]
 


    

