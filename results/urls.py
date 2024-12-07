from django.urls import path
from .views import ResultView
from .views import ColumnPreviewAPIView


urlpatterns = [
    path('', ResultView.as_view({'get': 'list'})),
    path('<int:pk>/', ResultView.as_view({'get': 'retrieve'})),
    path("preview-column/", ColumnPreviewAPIView.as_view(), name="preview_column"),
]