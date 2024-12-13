from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from .serializers import UserSerializer
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from fsp.settings import EMAIL_HOST_USER

# Create your views here.

class UserViewSet(ModelViewSet):
    #permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.save()
        # user.is_active=True
        # user.save()
#gg
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(email=email).exists():
            return Response({'details': ['Email уже зарегистрирован']}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
        token, created = Token.objects.get_or_create(user=user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        emailtoken = default_token_generator.make_token(user)

        # activation_link = f"http://localhost:5173/api/v1/users/activate/{uid}/{emailtoken}"
        # Вот это ссылку поменять на фронт прод внизу который, не только здесь
        activation_link = f"http://localhost:4173/email-verification?uuid={uid}&token={emailtoken}"
        send_mail(
            'Подтвердите регистрацию',
            f'Нажмите на ссылку чтобы подтвердить свою регистрацию: {activation_link}',
            EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return Response({'detail': 'Пользователь зарегистрирован. Пожалуйста, подтвердите email почту для активации аккаунта.', 'token': token.key}, status=HTTP_201_CREATED)
    
    def get_by_id(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def activate_account(self, request, uid64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Неправильная ссылка активации'}, status=HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Аккаунт активирован'}, status=HTTP_200_OK)
        else:
            return Response({'detail': 'Неверный токен'}, status=HTTP_400_BAD_REQUEST)

class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CheckToken(APIView):
    queryset = User.objects.all()

    def get(self, request):
        user = get_object_or_404(Token, key=request.headers['Authorization'].split()[-1]).user
        result = user is not None
        return Response({'detail': result})


class GetUserData(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = Token.objects.get(key=request.headers.get('Authorization', '').split()[-1]).user
        user_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
        }
        return Response(user_data)
