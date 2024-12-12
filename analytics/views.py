from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from results.models import Result
from results.serializers import ResultSerializer
from claims.models import Claim
from claims.serializers import ClaimSerializer
from country.models import Region
# Create your views here.

class AnalyticsResultsView(ModelViewSet):  
    queryset = Result.objects.all()
    regions = Region.objects.all()
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

    def search(self, request):
        results = self.queryset
        region = self.request.query_params.get('region', None)
        search_result = []

        for result in results:
            if result.sender_federation and result.sender_federation.region:
                if result.sender_federation.region.name and \
                    region.lower() in result.contest.organizer.region.name.lower():
                    search_result.append(result)
        
        serializer = self.get_serializer(search_result, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
        
    def avg_scores(self, request):
        regions = self.regions
        avg_scores = {}
        
        for reg in regions:
            reg_score = 0
            count = 0
            for res in Result.objects.filter(team__region__id=reg.id):
                reg_score += res.score
                count += 1
            
            if count > 0:
                avg_scores[reg.name] = reg_score / count
            else:
                avg_scores[reg.name] = 0
        
        return Response(avg_scores, status=HTTP_200_OK)
      
    
class AnalyticsClaimsView(ModelViewSet):  
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    
    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        sender_id = self.request.query_params.get('sender', None)
        receiver_id = self.request.query_params.get('receiver', None)
        _format = self.request.query_params.get('formats', None)
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


class RegionTeamsView(ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def get_regions_teams(self, request):
        result = Region.objects.all()
        ser = self.get_serializer(result, many=True)

        return Response(ser.data, status=HTTP_200_OK)