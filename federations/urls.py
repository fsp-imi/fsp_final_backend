from django.urls import path
from .views import FederationViewSet

urlpatterns = [
    path('', FederationViewSet.as_view({'get': 'list', 'post':'create'})),
    path('<int:pk>/', FederationViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('profile/', FederationViewSet.as_view({'get': 'profile'})),
]