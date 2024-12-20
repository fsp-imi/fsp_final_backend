### api/users/models.py
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # Ссылку поменять
    context = {
        'email': reset_password_token.user.email,
        'reset_password_url': f"https://fsp-imi-fsp-final-frontend-5466.twc1.net/password-reset-change/?token={reset_password_token.key}"
    }
    #email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('user_reset_password.txt', context)
    msg = EmailMultiAlternatives("Password Reset", email_plaintext_message, [], [reset_password_token.user.email])
    #msg.attach_alternative(email_html_message, "text/html")
    msg.send()
