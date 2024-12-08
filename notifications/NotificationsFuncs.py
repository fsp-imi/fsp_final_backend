from .models import Notification
from django.contrib.auth.models import User

def sendNotification(contest):
    from subscription.models import Subscription
    #users = Subscription.objects.filter(contest__id=contest.id).values_list('user__id', flat=True)
    users = User.objects.all()
    for user in User.objects.filter(id__in=users):
        Notification.objects.create(user=user, text=f'Обратите внимание! Информация по соревнованию \"{contest.program}\" изменилась!')
    
def sendClaimNotification(claim, text, user):
    Notification.objects.create(user=user, text=text)
