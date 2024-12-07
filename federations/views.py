from django.shortcuts import render
from django.http import Http404
from rest_framework.status import HTTP_201_CREATED
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fed = serializer.save()
        fed.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def profile(self, request, *args, **kwargs):
        federation = Federation.objects.filter(agent__id=request.user.id).first()
        if federation is None:
            raise Http404
        ser = self.get_serializer(federation)
        return Response(ser.data, status=200)
    
    def update(self, request, *args, **kwargs):
        federation = Federation.objects.filter(agent__id=request.user.id).first()
        if federation is None:
            raise Http404
        if federation.id == kwargs['pk'] or request.user.is_staff:
            super().update(request, *args, **kwargs)
            instance = self.get_object()
            ser = ser = self.get_serializer(instance)
            return Response(ser.data, status=200)
        return Response({'details': 'Вы не можете редактировать этот запись'}, status=403)
