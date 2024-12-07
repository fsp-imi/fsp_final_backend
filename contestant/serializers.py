from rest_framework import serializers
from .models import Team, Contestant


class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = [ 'id', 'fio']

class TeamSerializer(serializers.ModelSerializer):
    members = ContestantSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [ 'id', 'name', 'members']
