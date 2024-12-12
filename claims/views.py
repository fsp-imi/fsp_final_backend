from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from .models import Claim
from .serializers import ClaimSerializer
# Create your views here.

class ClaimView(ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    # permission_classes = [IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        claim = serializer.save()
        claim.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        claim = get_object_or_404(Claim, id=kwargs['pk'])
        new_status = request.data.get("status")

        if new_status not in Claim.Status.values:
            return Response(status=HTTP_400_BAD_REQUEST)
        can_update = (
            (not request.user.is_staff and claim.status in ["NEW", "MODERATE"] and new_status == "ONPROGRESS") or
            (request.user.is_staff and claim.status == "ONPROGRESS" and new_status != "NEW")
            )
        if can_update:
            claim.status = new_status
            claim.save()
            serializer = self.get_serializer(claim)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({"detail": "Нет доступа"},status=HTTP_404_NOT_FOUND)
        
    def get_by_id(self, request, *args, **kwargs):
        claim_id = kwargs.get('pk')
        claim = get_object_or_404(Claim, pk=claim_id)
        serializer = self.get_serializer(claim)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        claim = get_object_or_404(Claim, pk=kwargs['pk'])
        
        if  not request.user.is_staff:
            if claim.sender_federation is None or \
               claim.sender_federation.agent is None or \
               request.user.id != claim.sender_federation.agent.id:
               Response({"detail": "Нет доступа"},status=HTTP_404_NOT_FOUND)
           
        serializer = ClaimSerializer(claim, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        
class FSClaimsView(ModelViewSet):  
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    
    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        sender_id = self.request.query_params.get('sender', None)
        receiver_id = self.request.query_params.get('receiver', None)
        _format = self.request.query_params.get('formats', None)
        # _city = self.request.query_params.get('city', None)
        claims = self.queryset
        filters = {}

        if status:
            filters['status'] = status
        if sender_id:
            filters['sender_federation__id'] = sender_id
        if receiver_id:
            filters['receiver_federation__id'] = receiver_id
        if _format:
            filters['format'] = _format
        # if _city:
        #     filter['city'] = _city
        if filters:
            claims = claims.filter(**filters)
        
        return claims
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True) 
        return Response(serializer.data, status=HTTP_200_OK)

    def search(self, request):
        claims = self.queryset
        region = self.request.query_params.get('region', None)
        search_result = []

        for claim in claims:
            if claim.sender_federation and claim.sender_federation.region:
                if claim.sender_federation.region.name and \
                    region.lower() in claim.sender_federation.region.name.lower():
                    search_result.append(claim)
        
        serializer = self.get_serializer(search_result, many=True)
        return Response(serializer.data, status=HTTP_200_OK)