
from django.urls import path
from .views import SubscriptionView

urlpatterns = [
    path('', SubscriptionView.as_view({'get': 'list'})),
    path('subscribe/', SubscriptionView.as_view({'post': 'subscribe'})),
    path('<int:pk>/', SubscriptionView.as_view({'delete': 'delete'})),

]