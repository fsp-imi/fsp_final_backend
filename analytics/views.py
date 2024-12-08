from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from results.models import Result
from results.serializers import ResultSerializer
from claims.models import Claim
from claims.serializers import ClaimSerializer
# Create your views here.

class AnalyticsResultsView(ModelViewSet):  
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    
    def get_queryset(self):
        contest_id = self.request.query_params.get('contest', None)
        region_id = self.request.query_params.get('region', None)
        date_str = self.request.query_params.get('date', None)

        results = self.queryset
        filters = {}

        if contest_id:
            filters['contest__id'] = contest_id
        if region_id:
            filters['contest__federation__region__id'] = region_id
        if date_str:
            date = parse_date(date_str)
            if not date:
                raise ValidationError('Неверный формат даты. Ожидается YYYY-MM-DD.')
            filters['contest__start_time__date'] = date

        if filters:
            results = results.filter(**filters)
        
        return results

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True) 
        return Response(serializer.data, status=HTTP_200_OK)

    def search(self):
        results = self.queryset


    
class AnalyticsClaimsView(ModelViewSet):  
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    
    def get_queryset(self):
        __id = self.request.query_params.get('sadfs', None)
        _id = self.request.query_params.get('dasf', None)
        _str = self.request.query_params.get('dsaf', None)

        claims = self.queryset
        filters = {}

        if __id:
            filters['contest__id'] = __id
        if _id:
            filters['contest__federation__region__id'] = _id
        if _str:
            date = parse_date(_str)
            if not date:
                raise ValidationError('Неверный формат даты. Ожидается YYYY-MM-DD.')
            filters['contest__start_time__date'] = date

        if filters:
            claims = claims.filter(**filters)
        
        return claims
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True) 
        return Response(serializer.data, status=HTTP_200_OK)

    def search(self):
        claims = self.queryset

        