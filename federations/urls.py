from django.urls import path
from .views import FederationViewSet

urlpatterns = [
    path('', FederationViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', FederationViewSet.as_view({'get': 'retrieve'})),
    path('profile/', FederationViewSet.as_view({'get': 'profile'}))
]