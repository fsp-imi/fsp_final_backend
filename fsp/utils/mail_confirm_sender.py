from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

def send_activation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    print(reverse('activate', kwargs={'uid': uid, 'token': token}))
    activation_link = request.build_absolute_uri(
    reverse('activate', kwargs={'uid': uid, 'token': token})
)

    subject = 'Подтверждение регистрации'
    message = render_to_string('registration/activation_email.html', {
        'user': user,
        'activation_link': activation_link,
    })

    send_mail(
        subject,
        message,
        'info@beercut.ru',
        [user.email],
        fail_silently=False,
    )