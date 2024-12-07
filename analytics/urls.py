
from django.urls import path
from .views import SportTypeView, DisciplineView, ContestTypeView, AgeGroupView,ContestView, ContestDisciplineView, ContestAgeGroupView

urlpatterns = [
    path('', SportTypeView.as_view({'get': 'list'})),
]