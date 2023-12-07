from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm,RentalForm
from rental_api.models import *
import requests
from django.contrib import messages
from django.contrib.auth import login,logout
from .forms import LoginForm
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from rental_api.filters import IhaFilter



## user işlemleri ##

def logout_view(request):
    logout(request)
    messages.success(request, 'exit successful.')
    return redirect('anasayfa')

def login_view(request):  
    if not request.user.is_authenticated:
        form = LoginForm(request.POST or None)
        
        if form.is_valid():
            user = form.login(request)
            messages.success(request, 'login successful.')
            if user:
                login(request, user)

                return redirect('anasayfa')
            else:
                return redirect('login')
        return render(request, 'account/login.html', {'form': form})
    
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('anasayfa')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
                      ###
def contact(request):
    return render(request,"contact_page.html")

def list_ihas(request):
    iha_filter = IhaFilter(request.GET, queryset=Iha.objects.all())
    ihas = iha_filter.qs
   
    context = {
        'form': iha_filter.form,  
        'ihas': ihas,  
    }
    return render(request, "list_ihas.html", context)

def Main_Page(request):
    get_products_url=f'http://127.0.0.1:8000/api/ihas/'
    response = requests.get(get_products_url)
    if response.status_code == 200:
        data = response.json()
        return render(request,"index.html",{'data':data,})
    else:
        return render(request,"index.html")
    

def is_valid_rental_view(request):
    context={}
    id=request.user.id
    get_rents = f'http://127.0.0.1:8000/api/rental/user/{id}/'
    response = requests.get(get_rents)
    data = response.json()
    context['data']=data
    rent_list=[]
    now_renting_list=[]
    if response.status_code == 200:
    
        for data in data:
            iha_id=data['iha']

            
            get_product = f'http://127.0.0.1:8000/api/ihas/{iha_id}/'
            response = requests.get(get_product)
            product_data = response.json()

            rental_date_str = data['rental_date']
            return_date_str = data['return_date']

            rental_date = datetime.strptime(rental_date_str, '%Y-%m-%d')
            return_date = datetime.strptime(return_date_str, '%Y-%m-%d')
            now = datetime.now()
            if rental_date < now < return_date:
                        
                        if product_data not in now_renting_list:
                            now_renting_list.append(product_data)
                            
            
            else:
                if product_data not in rent_list:
                            rent_list.append(product_data)
                

        context['now_renting']=now_renting_list
        context['rent_list']=rent_list
       
       
       
        return render(request,"my_rentals.html",context)
    else:
         return render(request,"my_rentals.html")
    
def update_rental(request, id):
    
    rent_url=f'http://127.0.0.1:8000/api/rental/{id}/'
    resp=requests.get(rent_url)

    if resp.status_code == 200:
        data=resp.json()
        
    else:
        messages.error(request, 'Error')
        return redirect('rents')
    return render(request,"update_rentals.html",{'data':data})  
     


def create_rental_detail(request,id):
    form=RentalForm
    return render(request,'create_rental_detail.html',{'form':form,'id':id,})