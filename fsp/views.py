from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage

class UploadFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Файл не найден"}, status=400)

        # Сохраняем файл в хранилище
        file_name = default_storage.save(file.name, file)

        # Получаем URL файла
        file_url = default_storage.url(file_name)

        return Response({"url": file_url}, status=201)
