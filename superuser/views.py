from django.http import JsonResponse
from django.shortcuts import render,redirect
# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.signals import user_logged_in
import requests
from rental_api.models import *
from rent_app.forms import *
from superuser.forms import IhaForm
from django.db.models import Count
from pprint import pprint
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django_serverside_datatable.views import ServerSideDatatableView


@user_passes_test(lambda u: u.is_superuser, login_url='anasayfa')
def list_ihas_admin(request):
    list_ihas_url='http://127.0.0.1:8000/api/ihas/'   
    response = requests.get(list_ihas_url)
    listed_ihas=response.json()

    return render(request,'iha_list_admin.html',{'listed_ihas':listed_ihas,})
@user_passes_test(lambda u: u.is_superuser, login_url='anasayfa')
def iha_update_superuser(request,id):
   
    url=f"http://127.0.0.1:8000/api/ihas/{id}/"
    iha_types=Ihatype.objects.all()
    response=requests.get(url)
    if not response.status_code==200:
        redirect('home') 
    data=response.json()
 
    return render(request,"admin_iha_update.html",{'data':data,'iha_types':iha_types})
def admin_rental_update(request,id):

    
    rent_url=f'http://127.0.0.1:8000/api/rental/{id}/'
    resp=requests.get(rent_url)

    if resp.status_code == 200:
        data=resp.json()
        
    else:
       
        return redirect('rents')
    return render(request,"admin_rental_update.html",{'data':data}) 
@user_passes_test(lambda u: u.is_superuser, login_url='anasayfa')
@receiver(user_logged_in)
def track_user_login(sender, user, **kwargs):
    UserLogin.objects.create(user=user)

@user_passes_test(lambda u: u.is_superuser, login_url='anasayfa')
def user_activity_data(request):
    rental_activity = Rental.objects \
        .values('user__username') \
        .annotate(rental_count=Count('id')) \
        .filter(rental_count__gt=0) \
        .order_by('user__username')

    return JsonResponse({
        'rental_activity': list(rental_activity)
    })
@user_passes_test(lambda u: u.is_superuser, login_url='anasayfa')
def index(request):
    return render(request,"superuser_index.html")
@user_passes_test(lambda u: u.is_superuser, login_url='anasayfa')
def create_iha(request):
    form = IhaForm()
    return render(request,"create_iha.html",{'form':form})


@user_passes_test(lambda u: u.is_superuser, login_url='anasayfa')
def list_contact_admin(request):
    message_url=f'http://127.0.0.1:8000/api/contact/'
    response=requests.get(message_url)
    if not response.status_code==200:
        redirect('admin_index')
    messages=response.json()
    for message in messages:
        created_at_datetime = datetime.fromisoformat(message['created_at'].rstrip('Z'))
        adjusted_datetime = created_at_datetime + timedelta(hours=3)
        message['created_at']=adjusted_datetime.strftime("%Y-%m-%d %H:%M")
   
    return render(request,"admin_contact.html",{'messages':messages,})

@user_passes_test(lambda u: u.is_superuser, login_url='anasayfa')
def list_rentals_admin(request):
    rentals_url=f'http://127.0.0.1:8000/api/rental/'
    response=requests.get(rentals_url)
    if not response.status_code == 200:
        redirect('admin_index')
    all_rents=response.json()
    return render(request, 'list_rentals.html',{'all_rents':all_rents,})