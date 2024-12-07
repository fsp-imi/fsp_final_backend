from .models import Result
from .serializers import ResultSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from .parse_file import parse_file


# Create your views here.

class ResultView(ModelViewSet):
    #permission_classes = [IsAuthenticated]

    queryset = Result.objects.all()
    serializer_class = ResultSerializer    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        results = serializer.save()
        results.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
