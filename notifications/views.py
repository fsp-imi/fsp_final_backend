from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR


# Create your views here.
class NotificationView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get(self, request):
        queryset = Notification.objects.filter(user__id=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def delete(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.delete()
            return Response({"result":True}, status=HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            return Response({"result":False, "errors":"Уведомление не найдено"},status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"errors": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
