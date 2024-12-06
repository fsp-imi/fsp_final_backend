from django.contrib import admin
from django.urls import path
from .views import UserViewSet, CheckToken, GetUserData, UserProfile
from rest_framework.authtoken import views

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'})),
    path('create/', UserViewSet.as_view({'post': 'create'})),
    path('api-token-auth/', views.obtain_auth_token),
    path('check-token/', CheckToken.as_view()),
    path('get-user/', GetUserData.as_view()),
    path('profile/', UserProfile.as_view()),
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
]