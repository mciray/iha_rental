from django import forms
from django.contrib.auth import authenticate
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rental_api.models import *

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError("Yanlış kullanıcı adı veya şifre")
        return self.cleaned_data


    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
    

class CustomUserCreationForm(SignupForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email field is required.")
        return email

    def save(self, request):
        email_address_obj = super(CustomUserCreationForm, self).save(request)
        return email_address_obj

   

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['user', 'iha', 'renter_name', 'rental_date', 'return_date', 'subject']


    widgets = {
        'user': forms.Select(attrs={'class': 'form-control'}),
        'iha': forms.Select(attrs={'class': 'form-control'}),
        'renter_name': forms.TextInput(attrs={'class': 'form-control'}),
        'rental_date': forms.DateInput(attrs={'class': 'form-control'}),
        'return_date': forms.DateInput(attrs={'class': 'form-control'}),
        'subject': forms.Textarea(attrs={'class': 'form-control'}),
    }       
