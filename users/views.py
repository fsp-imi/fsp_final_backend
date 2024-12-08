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

# Create your views here.

class UserViewSet(ModelViewSet):
    #permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active=False
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        send_activation_email(user, request)
        return Response({'detail': 'Проверьте почту для активации аккаунта.'}, status=HTTP_201_CREATED)
        # return Response({'token': token.key}, status=HTTP_201_CREATED)
 
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
