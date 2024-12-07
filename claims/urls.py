from django.urls import path
from .views import ClaimView

urlpatterns = [
    path('', ClaimView.as_view({'get': 'list'})),
    path('<int:pk>/', ClaimView.as_view({'get': 'get_by_id', 'post': 'post'})),
]
