"""
URL configuration for rental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rent_app.views import *
from django.urls import path,include, re_path
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Main_Page,name="anasayfa"),

    ## admin 
    path('api/',include('rental_api.urls')), 

    path('accounts/', include('allauth.urls')),
    path('logout/',logout_view,name="logout"),
    path('login/', login_view, name='login'),
    path('Contacts/',login_required(contact),name="contact"),
  

    
 ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


