from django.shortcuts import render
from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import FederationSerializer
from .models import Federation

# Create your views here.

class FederationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Federation.objects.all()
    serializer_class = FederationSerializer

    def profile(self, request, *args, **kwargs):
        federation = Federation.objects.filter(agent__id=request.user.id).first()
        if federation is None:
            raise Http404
        ser = self.get_serializer(federation)
        return Response(ser.data, status=200)
