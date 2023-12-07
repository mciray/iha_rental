from django.urls import path,include,re_path
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    path("", Index, name="home"),
    path('index/graph/',user_activity_data,name="user_activity_data"),  
    path("iha/create/", create_iha, name="admin_create_iha")
 ]

