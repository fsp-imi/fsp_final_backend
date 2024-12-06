from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .views import FederationSerializer
from .models import Federation

# Create your views here.

class CountryViewSet(ModelViewSet):
    #permission_classes = [IsAdminUser]

    queryset = Federation.objects.all()
    serializer_class = FederationSerializer
