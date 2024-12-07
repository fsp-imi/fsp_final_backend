from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import Claim
from .serializers import ClaimSerializer
# Create your views here.

class ClaimView(ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = [IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        claim = serializer.save()
        claim.is_active=False
        claim.save()
        token, created = Token.objects.get_or_create(claim=claim)
        send_activation_email(user, request)
        return Response({'detail': 'Проверьте почту для активации аккаунта.'}, status=HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        claim = get_object_or_404(Claim, id=kwargs['pk'])
        new_status = request.data.get("status")

        if new_status not in Claim.Status.values:
            return Response(status=HTTP_400_BAD_REQUEST)

        claim.status = new_status
        claim.save()
        
        serializer = self.get_serializer(claim)

        return Response(serializer.data, status=HTTP_200_OK)
        
    def get_by_id(self, request, *args, **kwargs):
        claim_id = kwargs.get('pk')
        claim = get_object_or_404(Claim, pk=claim_id)
        serializer = self.get_serializer(claim)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        
