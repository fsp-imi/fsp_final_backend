from rest_framework import serializers
from .models import ClaimFile, Claim

class ClaimFileSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClaimFile
        fields = ['id', 'claim', 'file', 'description']

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['id', 'name', 'start_time', 'end_time', 'place', 'format', 'status']