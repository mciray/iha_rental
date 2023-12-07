import django_filters
from .models import Iha
from django import forms

class IhaFilter(django_filters.FilterSet):
    class Meta:
        model=Iha
        fields=['iha_type']
      