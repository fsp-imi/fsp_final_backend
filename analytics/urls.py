from django.urls import path
from .views import FilterView

urlpatterns = [
    path('', FilterView.as_view({'get': 'list'})),
]