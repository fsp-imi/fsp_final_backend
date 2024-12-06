from django.shortcuts import render
from rest_framework import response
from rest_framework.viewsets import ModelViewSet
from .models import Claim
from .serializers import ClaimSerializer
# Create your views here.

class ClaimView(ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer