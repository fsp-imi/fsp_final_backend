from rest_framework import serializers
from .models import ClaimFile, Claim
from contests.models import Contest

class ClaimFileSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClaimFile
        fields = ['id', 'claim', 'file', 'description']

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['id', 'name', 'sender_federation', 'receiver_federation', 'start_time',
                  'end_time', 'place', 'format', 'status', 'contest_char', 'contest_type',
                  'contest_discipline', 'contest_age_group']
        
        def create(self, validated_data):
            name = validated_data.get('name')
            sender_federation = validated_data.get('sender_federation')
            receiver_federation = validated_data.get('receiver_federation')
            start_time = validated_data.get('start_time')
            end_time = validated_data.get('end_time')
            place = validated_data.get('place', None)
            format = validated_data.get('format', Contest.ContestFormat.ONL)
            status = validated_data.get('status', Claim.Status.NEW)
            contest_char = validated_data.get('contest_char', Contest.ContestCharateristic.PERSONAL)
            contest_type = validated_data.get('contest_type', None)
            contest_discipline = validated_data.get('contest_discipline', None)
            contest_age_group = validated_data.get('contest_age_group', None)
            
            claim = self.Meta.model(
                name=name,
                sender_federation=sender_federation,
                receiver_federation=receiver_federation,
                start_time=start_time,
                end_time=end_time,
                place=place,
                format=format,
                status=status,
                contest_char=contest_char,
                contest_type=contest_type
            )
            claim.save()
            if contest_discipline:
                claim.contest_discipline.set(contest_discipline)
            if contest_age_group:
                claim.contest_age_group.set(contest_age_group)
            return claim