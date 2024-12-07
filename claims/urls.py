from django.urls import path
from .views import ClaimView

urlpatterns = [
    path('', ClaimView.as_view({'get': 'list', 'post':'create'})),
    path('<int:pk>/', ClaimView.as_view({'get': 'get_by_id', 
                                         'put': 'put', 
                                         'post': 'post'})),
]
