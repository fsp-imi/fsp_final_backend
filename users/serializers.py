from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name', 'is_active', 'password', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True},
            #'username': {'read_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=validated_data.get('is_active', False),
            password=validated_data['password']
        )
        return user
