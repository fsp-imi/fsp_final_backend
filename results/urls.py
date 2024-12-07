from django.urls import path
from .views import ResultView

urlpatterns = [
    path('', ResultView.as_view({'get': 'list'})),
    path('<int:pk>/', ResultView.as_view({'get': 'retrieve'})),
]