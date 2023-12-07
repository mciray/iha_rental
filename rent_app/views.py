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
    return redirect('anasayfa')

def Main_Page(request):
   
    get_products_url=f'http://127.0.0.1:8000/api/ihas/'
    response = requests.get(get_products_url)
    if response.status_code == 200:
        data = response.json()
        return render(request,"index.html",{'data':data,})
    else:

        return render(request,"index.html")
    


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

def contact(request):
    return render(request,"contact_page.html")

