from django.urls import path
from .views import AnalyticsResultsView, AnalyticsClaimsView

urlpatterns = [
    path('results/', AnalyticsResultsView.as_view({'get': 'list', 'post':'search'})),
    path('results/average-scores', AnalyticsResultsView.as_view({'get': 'avg_scores'})),
    path('claims/', AnalyticsClaimsView.as_view({'get': 'list', 'post':'search'})),
]