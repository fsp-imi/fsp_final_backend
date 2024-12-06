from rest_framework import serializers
from .models import SportType, Discipline, ContestType, AgeGroup, Contest


class SportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportType
        fields = ['id', 'name']


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'sport_type', 'name']


class ContestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestType
        fields = ['id', 'name']


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = ['id', 'contest', 'gender', 'start', 'end']


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['id', 'program', 'code', 'start', 'end', 'place', 'country', 'contestants', 'contest_type', 'male', 'female']

        