from django.urls import path
from .views import AnalyticsResultsView, AnalyticsClaimsView

urlpatterns = [
    path('results/', AnalyticsResultsView.as_view({'get': 'list', 'post':'search'})),
    path('claims/', AnalyticsClaimsView.as_view({'get': 'list', 'post':'search'})),
]