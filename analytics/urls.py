
from django.urls import path
from .views import SportTypeView, DisciplineView, ContestTypeView, AgeGroupView,ContestView, ContestDisciplineView, ContestAgeGroupView

urlpatterns = [
    path('result/filter/', SportTypeView.as_view({'get': 'filter'})),
]