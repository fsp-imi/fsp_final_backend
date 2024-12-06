from rest_framework import serializers
from .models import Country, District, Region, City


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)
    district_id = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), source="district", write_only=True)

    class Meta:
        model = Region
        fields = ['id', 'district_id','district', 'name']


class CitySerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), source="region", write_only=True)

    class Meta:
        model = City
        fields = ['id', 'region_id', 'region', 'name']