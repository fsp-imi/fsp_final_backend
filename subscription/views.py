from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from .models import Subscription
from .serializers import SubscriptionSerializer
from contests.models import Contest

# Create your views here.
class SubscriptionView(ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = Subscription.objects.filter(user__id=request.user.id)
        ser = self.get_serializer(queryset, many=True)
        return Response(ser.data, status=200)
    
    def delete(self, request, subscription_id):
        try:
            notification = Subscription.objects.get(contest__id=subscription_id, user=request.user)
            notification.delete()
            return Response({"result":True}, status=HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response({"result":False, "errors":"Подписка не найдена"},status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"errors": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    
#    @action(detail=True, method=['post'])
    def subscribe(self, request):
        result = {'result': False}
        print(request.data['subscribe'])
        print(isinstance(request.data['subscribe'], list))
        print(request.method)
        if request.method == 'POST':
            if 'subscribe' in request.data:
                try:
                    for contest in Contest.objects.filter(id__in=request.data['subscribe']):
                        Subscription.objects.create(user=request.user, contest=contest)
                    result['result'] = True
                except:
                    result['error'] = 'Список идентификаторов неправильно задан!'
            return Response(result, status=200)
        return Response(result, status=200)