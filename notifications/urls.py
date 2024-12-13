from django.urls import path
from .views import NotificationView

urlpatterns = [
    path('', NotificationView.as_view({'get': 'get'})),
    path('<int:notification_id>/', NotificationView.as_view({'delete': 'delete'})),
]