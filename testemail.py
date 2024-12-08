from fsp.wsgi import application
from django.core.mail import send_mail

send_mail(
    'Тестовое письмо',
    'Это тестовое письмо от Django.',
    'info@beercut.ru',  # Отправитель
    ['vv.everstov@s-vfu.ru'],  # Получатель
    fail_silently=False,
)