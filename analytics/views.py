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


class RegionTeamsView(ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def get_regions_teams(self, request):
        result = Region.objects.all()
        ser = self.get_serializer(result, many=True)

        return Response(ser.data, status=HTTP_200_OK)
