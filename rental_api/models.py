

from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save



class UserLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} logged in at {self.timestamp}"

class ContactMessage(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        
        verbose_name = "Contact"
        verbose_name_plural = "Contact"
    def __str__(self):
        if self.user:
            return f"{self.subject} - {self.user.username}"
        else:
            return self.name
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        super(ContactMessage, self).save(*args, **kwargs)
class Ihatype(models.Model):
    name =models.CharField(max_length=150,blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
class Iha(models.Model):
    
    photo=models.ImageField(upload_to="media/",blank=True, null=True)
    iha_type=models.ForeignKey(Ihatype,on_delete=models.SET_NULL,blank=True, null=True)
    brand = models.CharField(max_length=100)
    weight=models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class Rental(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True, null=True)
    iha = models.ForeignKey(Iha,on_delete=models.SET_NULL,null=True)
    renter_name = models.CharField(max_length=100)
    rental_date = models.DateField()
    return_date = models.DateField()
    subject=models.TextField(blank=True, null=True)
    date_difference=models.IntegerField(blank=True, null=True)
    total_price=models.IntegerField(blank=True, null=True)
   
    def calculate_total_price(self):
        if self.date_difference is None:
            self.date_difference = (self.return_date - self.rental_date).days

        self.total_price = self.date_difference * self.iha.price_per_day
        return self.total_price

    def save(self, *args, **kwargs):
      
        self.calculate_total_price()
        super(Rental, self).save(*args, **kwargs)
