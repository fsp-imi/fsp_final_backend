from django.urls import path
from .views import AnalyticsResultsView

urlpatterns = [
    path('average-scores/', AnalyticsResultsView.as_view({'get': 'avg_scores'})),
]