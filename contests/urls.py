
from django.urls import path
from .views import SportTypeView, DisciplineView, ContestTypeView, AgeGroupView,ContestView

urlpatterns = [
    path('sporttypes/', SportTypeView.as_view({'get': 'list'})),
    path('sporttypes/<int:pk>', SportTypeView.as_view({'get': 'retrieve'})),
    path('disciplines/', DisciplineView.as_view({'get': 'list'})),
    path('disciplines/<int:pk>', DisciplineView.as_view({'get': 'retrieve'})),
    path('disciplines/by_sport_type/', DisciplineView.as_view({'get': 'get_disciplines_by_sport_type'})),
    path('contesttypes/', ContestTypeView.as_view({'get': 'list'})),
    path('contesttypes/<int:pk>', ContestTypeView.as_view({'get': 'retrieve'})),
    path('agegroups/', AgeGroupView.as_view({'get': 'list'})),
    path('agegroups/<int:pk>', AgeGroupView.as_view({'get': 'retrieve'})),
    path('contests/', ContestView.as_view({'get': 'list'})),
    path('contests/<int:pk>', ContestView.as_view({'get': 'retrieve'})),
    path('contests/filter', ContestView.as_view({'get': 'get_filter_data'})),
]