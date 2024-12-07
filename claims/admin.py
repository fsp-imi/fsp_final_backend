from django.contrib import admin
from .models import Claim, ClaimFile

# Register your models here.

admin.site.register(Claim)
admin.site.register(ClaimFile)