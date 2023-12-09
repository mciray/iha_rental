from django import forms
from rental_api.models import *

class IhaForm(forms.ModelForm):
    class Meta:
        model = Iha
        fields = ['photo', 'iha_type', 'brand', 'weight', 'model', 'year','price_per_day']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'iha_type': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
        }
