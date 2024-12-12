from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from .serializers import UserSerializer
from fsp.utils.mail_confirm_sender import send_activation_email
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Create your views here.

class UserViewSet(ModelViewSet):
    #permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active=True
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        # send_activation_email(user, request)
        # return Response({'detail': 'Проверьте почту для активации аккаунта.'}, status=HTTP_201_CREATED)
        return Response({'token': token.key}, status=HTTP_201_CREATED)
#gg
        # username = request.data.get('username')
        # email = request.data.get('email')
        # password = request.data.get('password')

        # if User.objects.filter(email=email).exists():
        #     return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

        # user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
        # uid = urlsafe_base64_encode(force_bytes(user.pk))
        # token = default_token_generator.make_token(user)

        # activation_link = f"{fsp.settings.FRONTEND_URL}/activate/{uid}/{token}"
        # send_mail(
        #     'Confirm your registration',
        #     f'Click the link to confirm your registration: {activation_link}',
        #     settings.EMAIL_HOST_USER,
        #     [email],
        #     fail_silently=False,
        # )

        # return Response({'message': 'User registered. Please confirm your email to activate your account.'}, status=status.HTTP_201_CREATED)
    def get_by_id(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def activate_account(self, request, uid64, token):
        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response('Аккаунт активирован!')
        else:
            return Response('Ссылка активации недействительна.')


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
