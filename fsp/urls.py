"""
URL configuration for fsp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

from s3.views import UploadFileView


apiv1 = [
    path('users/', include('users.urls')),
    path('contests/', include('contests.urls')),
    path('countries/', include('country.urls')),
    path('notifications/', include('notifications.urls')),
    path('subscriptions/', include('subscription.urls')),
    path('claims/', include('claims.urls')),
    path('federations/', include('federations.urls')),
    path('results/', include('results.urls')),
    path("upload/", UploadFileView.as_view(), name="upload_file"),
    path("analytics/", include('analytics.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((apiv1, 'fsp'), namespace='apiv1')),
]
