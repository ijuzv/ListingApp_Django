from django.contrib import admin
from .models import CustomUser, Vehicle, VehicleImage

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Vehicle)
admin.site.register(VehicleImage)
