from django.urls import path
from .views import ResultView, FileUploadView

urlpatterns = [
    path('', ResultView.as_view({'get': 'list'})),
    path('<int:pk>/', ResultView.as_view({'get': 'retrieve'})),
    path('uploadresults/', FileUploadView.as_view()),
]