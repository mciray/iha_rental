from django.shortcuts import render
from rest_framework import parsers
# Create your views here.
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import ContactMessage
from rest_framework import generics
from rest_framework import viewsets
from .models import *
from .serializers import ContactMessageSerializer,RentalSerializer,IhaSerializer,RentalDetailSerializer,IhaTypeSerializers




class ContactCreateAPIView(generics.CreateAPIView):
    serializer_class=ContactMessageSerializer

class ContactAPIView(APIView):
    def get(self, request, *args, **kwargs):
        contacts = ContactMessage.objects.all()
        serializer=ContactMessageSerializer(contacts,many=True)
        return Response(serializer.data)



class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalDetailSerializer
    def perform_update(self, serializer):
        instance=serializer.save()
        start_date = instance.rental_date
        end_date = instance.return_date
        total = (end_date - start_date).days 
        if total < 0:
                print("Hatalı tarih aralığı")
                return Response(serializer.errors, status=status.HTTP_205_RESET_CONTENT)
        else:
            new_total_price = total * instance.iha.price_per_day
            instance.date_difference = total
            instance.total_price = new_total_price
            instance.save()  

            return Response(serializer.data, status=status.HTTP_200_OK)
        

    
class RentalDeleteAPIView(generics.DestroyAPIView):
    lookup_field="pk"
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

           








class IhaViewSet(viewsets.ModelViewSet):
    queryset = Iha.objects.all()
    serializer_class = IhaSerializer

     



class ContactViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer


class IhaTypeCreateAPIView(generics.CreateAPIView):
    queryset = Ihatype.objects.all()
    serializer_class =IhaTypeSerializers