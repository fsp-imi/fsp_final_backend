from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
from django.db.models import Avg
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.pagination import PageNumberPagination
from results.models import Result
from results.serializers import ResultSerializer
from claims.models import Claim
from claims.serializers import ClaimSerializer
from country.models import Region
from contests.models import Contest
from contestant.models import Team
# Create your views here.

   
class AnalyticsPagination(PageNumberPagination):
    page_size = 1  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Позволяет задавать размер страницы через параметр запроса
    max_page_size = 100  # Максимальное количество элементов на странице


class AnalyticsResultsView(ModelViewSet):
    pagination_class = AnalyticsPagination  # Указываем класс пагинации
    
    def avg_scores(self, request):
        region_ids = request.query_params.getlist('region')
        regions = Region.objects.filter(id__in=region_ids) if region_ids else Region.objects.all()
        
        results = Result.objects.filter(team__region__id__in=regions.values_list('id', flat=True))
        avg_scores = (
            results.values('team__region__name')
            .annotate(avg_score=Avg('score'))
            .order_by('team__region__name')
        )
        
        paginator = self.pagination_class()
        paginated_avg_scores = paginator.paginate_queryset(avg_scores, request, view=self)
        
        avg_scores_dict = [{item['team__region__name']: item['avg_score']} for item in paginated_avg_scores]
        
        return paginator.get_paginated_response(avg_scores_dict)


class RegionTeamsView(ModelViewSet):
    pagination_class = AnalyticsPagination

    def get_regions_teams(self, request):
        region_ids = request.query_params.getlist('region')
        
        if region_ids:
            regions = Region.objects.filter(id__in=region_ids)
        else:
            regions = Region.objects.all()
        
        teams = Team.objects.all()
        result = []

        for region in regions:
            count = sum(1 for team in teams if team.region and team.region.name == region.name)
            if count > 0:
                result.append({'region': region.name, 'team_count': count})

        paginator = self.pagination_class()
        paginated_result = paginator.paginate_queryset(result, request, view=self)

        return paginator.get_paginated_response(paginated_result)
