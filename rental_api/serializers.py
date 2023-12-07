from rest_framework import serializers
from .models import *

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
class RentalDetailSerializer(serializers.ModelSerializer):
    iha=serializers.SerializerMethodField()
    class Meta:
        model = Rental
        fields = '__all__'
    def get_iha(self,object):
        iha_serilize=IhaSerializer(object.iha)
        return iha_serilize.data
class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'
        
class IhaSerializer(serializers.ModelSerializer):
    iha_type=serializers.SerializerMethodField()
    class Meta:
        model = Iha
        fields = '__all__'
    def get_iha_type(self,object):
        iha_serilize=IhaTypeSerializers(object.iha_type)
        return iha_serilize.data
    
class IhaTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ihatype
        fields = ['id','name']