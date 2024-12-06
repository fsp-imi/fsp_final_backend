from django.contrib import admin
from .models import Country, District, Region, City
# Register your models here.


admin.site.register(Country)
admin.site.register(District)
admin.site.register(Region)
admin.site.register(City)