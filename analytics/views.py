from django.db.models import Avg
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from results.models import Result
from country.models import Region
from contestant.models import Team
from utils import get_page_object
# Create your views here.


class AnalyticsResultsView(ModelViewSet):
    
    def avg_scores(self, request):
        region_ids = request.query_params.getlist('region')
        regions = Region.objects.filter(id__in=region_ids) if region_ids else Region.objects.all()
        results = Result.objects.filter(team__region__id__in=regions.values_list('id', flat=True))
        
        avg_scores = (
            results.values('team__region__name')
            .annotate(avg_score=Avg('score'))
            .order_by('team__region__name')
        )
        
        page = int(request.query_params.get('page', 1))  # Текущая страница
        amount = int(request.query_params.get('amount', 10))  # Количество записей на страницу
        paginated_scores, cur_page, per_page, total_pages = get_page_object(avg_scores, page, amount)
        avg_scores_dict = [{item['team__region__name']: item['avg_score']} for item in paginated_scores]

        response_data = {
            "data": avg_scores_dict,
            "pages": {
                "total": total_pages,
                "per_page": per_page,
                "cur_page": cur_page,
            }
        }

        return Response(response_data)

class RegionTeamsView(ModelViewSet):
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
                result.append({region.name: count})
        page = int(request.query_params.get('page', 1))
        amount = int(request.query_params.get('amount', 10))
        paginated_result, cur_page, per_page, total_pages = get_page_object(result, page, amount)
        response_data = {
            "data": paginated_result,
            "pages": {
                "total": total_pages,
                "per_page": per_page,
                "cur_page": cur_page,
            }
        }

        return Response(response_data)