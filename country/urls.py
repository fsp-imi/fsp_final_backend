from django.urls import path
from .views import CountryViewSet, DistrictViewSet, RegionViewSet, CityViewSet

urlpatterns = [
    path('countries/', CountryViewSet.as_view({'get': 'list'})),
    path('districts/', DistrictViewSet.as_view({'get': 'list'})),
    path('regions/', RegionViewSet.as_view({'get': 'list'})),
    path('cities/', CityViewSet.as_view({'get': 'list'})),
    path('countries/<int:pk>', CountryViewSet.as_view({'get': 'retrieve'})),
    path('districts/<int:pk>', DistrictViewSet.as_view({'get': 'retrieve'})),
    path('regions/<int:pk>', RegionViewSet.as_view({'get': 'retrieve'})),
    path('cities/<int:pk>', CityViewSet.as_view({'get': 'retrieve'})),
]