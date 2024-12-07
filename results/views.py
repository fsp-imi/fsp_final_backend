from .models import Result
from .serializers import ResultSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from rest_framework.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from .parse_file import parse_file

import pandas as pd
import numpy as np

# Create your views here.

class ResultView(ModelViewSet):
    #permission_classes = [IsAuthenticated]

    queryset = Result.objects.all()
    serializer_class = ResultSerializer   
    def create(self, request, *args, **kwargs):

        contest = request.data.get('contest')
        teams = request.data.get('team')
        scores = request.data.get('score')

        if not contest or not teams or not scores:
            raise ValidationError("Необходимо передать 'contest', 'teams' и 'scores'.")

        if len(teams) != len(scores):
            raise ValidationError("Длина списков 'teams' и 'scores' должна совпадать.")

        results = []
        for team_id, score in zip(teams, scores):
            result = Result(
                contest_id=contest,
                team_id=team_id,
                score=score
            )
            result.save()
            results.append(result)

        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data, status=HTTP_201_CREATED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        results = serializer.save()
        results.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

class ColumnPreviewAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Получаем параметры из запроса
        file = request.FILES.get("file")
        column_index = int(request.data.get("column_index"))
        header = request.data.get("header", "Column")
        num_rows = int(request.data.get("num_rows", 5))  # Количество строк (по умолчанию 5)

        if not file:
            return Response({"error": "Файл не предоставлен."}, status=400)

        try:
            # Определяем тип файла и читаем его
            file_extension = file.name.split('.')[-1].lower()
            if file_extension in ['xls', 'xlsx']:
                df = pd.read_excel(file)
            elif file_extension == 'csv':
                df = pd.read_csv(file)
            else:
                return Response({"error": "Неподдерживаемый тип файла."}, status=400)

            # Проверяем, существует ли указанный столбец
            if column_index < 0 or column_index >= len(df.columns):
                return Response({"error": "Неверный индекс столбца."}, status=400)

            # Извлекаем данные из столбца
            column_data = df.iloc[:, column_index].head(num_rows)
            
            # Обрабатываем значения NaN, заменяя их на None
            column_data = column_data.replace({np.nan: None}).tolist()
            
            result = {
                header: column_data
            }

            return Response(result, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
