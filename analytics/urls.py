from django.urls import path
from .views import AnalyticsResultsView, RegionTeamsView

urlpatterns = [
    path('average-scores/', AnalyticsResultsView.as_view({'get': 'avg_scores'})),
    path('region-teams/', RegionTeamsView.as_view({'get': 'get_regions_teams'})),
]