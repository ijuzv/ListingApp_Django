from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import datetime

# Choices
products = [('Car', 'Car'), ('Bike', 'Bike')]
model_choices = [(r, str(r)) for r in range(1984, datetime.date.today().year + 1)]
brand_choices = [(brand, brand) for brand in ['Honda', 'Suzuki', 'Hero', 'Yamaha', 'Ampere', 'Ather', 'Uber', 'Royal Enfield', 'Jawa']]
fuel_choices = [('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric')]
transmission_choices = [('Manual', 'Manual'), ('Automatic', 'Automatic')]
user_type_choices = [('Customer', 'Customer'), ('Dealer', 'Dealer')]

# User model
class CustomUser(models.Model):
    username = models.CharField(max_length=254)
    profile = models.ImageField(upload_to='profile/', blank=True, null=True)
    contact = models.BigIntegerField(unique=True)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=254)
    user_type = models.CharField(max_length=10, choices=user_type_choices, default='Customer')
    password = models.CharField(max_length=150, blank=False, null=False)

    class Meta:
        db_table = 'customuser'
        app_label = 'products'
        
    def __str__(self):
        return self.user

# Vehicle model
class Vehicle(models.Model):
    product_type = models.CharField(_('product_type'), choices=products, max_length=50)
    brand = models.CharField(_('brand'), choices=brand_choices, max_length=50)
    model_year = models.IntegerField(_('model year'), choices=model_choices)
    fuel_type = models.CharField(_('fuel type'), choices=fuel_choices, max_length=10)
    km_driven = models.IntegerField()
    title = models.CharField(max_length=56, blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    owners = models.IntegerField()
    insurance = models.BooleanField(default=False)

    class Meta:
        db_table = 'vehicle'
        app_label = 'products'
        
    def __str__(self):
        return self.title

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=False, blank=False)
    
    class Meta:
        db_table = 'vehicle_images'
        app_label = 'products'

    def __str__(self):
        return f"Image for {self.vehicle}"