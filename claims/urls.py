from django.urls import path
from .views import ClaimView

urlpatterns = [
    path('', ClaimView.as_view({'get': 'list'})),
]
