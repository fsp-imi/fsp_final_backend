from django.contrib import admin
from .models import SportType, Discipline, ContestType, AgeGroup, Contest, ContestDiscipline
# Register your models here.

admin.site.register(SportType)
admin.site.register(Discipline)
admin.site.register(ContestType)
admin.site.register(AgeGroup)
admin.site.register(Contest)
admin.site.register(ContestDiscipline)