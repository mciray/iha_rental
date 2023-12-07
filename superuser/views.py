from django.http import JsonResponse
from django.shortcuts import render,redirect
from rental_api.models import *
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from .forms import IhaForm
# Create your views here.


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

def Index(request):
    return render(request,"superuser_index.html")

def create_iha(request):
    form = IhaForm()
    return render(request,"admin_create_iha.html",{'form':form})