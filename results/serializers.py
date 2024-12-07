from rest_framework import serializers
from .models import Result
from contests.models import Contest
from contests.serializers import ContestSerializer
from contestant.serializers import TeamSerializer
from contestant.models import Team


class ResultSerializer(serializers.ModelSerializer):
    contest = ContestSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Result
        fields = [ 'id', 'contest', 'team', 'score']