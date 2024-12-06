from django.shortcuts import render
from .serializers import CountrySerializer, DistrictSerializer, RegionSerializer, CitySerializer
from .models import Country, District, Region, City
from rest_framework.viewsets import ModelViewSet
# Create your views here.


class CountryViewSet(ModelViewSet):
    #permission_classes = [IsAdminUser]

    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class DistrictViewSet(ModelViewSet):
    #permission_classes = [IsAdminUser]

    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class RegionViewSet(ModelViewSet):
    #permission_classes = [IsAdminUser]

    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class CityViewSet(ModelViewSet):
    #permission_classes = [IsAdminUser]

    queryset = City.objects.all()
    serializer_class = CitySerializer
