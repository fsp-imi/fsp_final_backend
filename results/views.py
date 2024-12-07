from .models import Result
from .serializers import ResultSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from .parse_file import parse_file

# Create your views here.

class ResultView(ModelViewSet):
    #permission_classes = [IsAuthenticated]

    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        dir = '/upload/'
        for filename, file_obj in request.FILES.items():
            with open(dir + filename, 'wb') as f:
                f.write(file_obj.read())
            parse_file(dir + filename)
        # do some stuff with uploaded file
        return Response(status=204)