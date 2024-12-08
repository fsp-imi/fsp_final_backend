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

    def parse_column_ranges(self, column_range: str) -> list:
        """
        Парсит строку с диапазонами столбцов и возвращает список индексов.
        Пример входных данных: "3, 5, 6-12, , 312"
        """
        indices = []
        try:
            for part in column_range.split(','):
                part = part.strip()
                if '-' in part:  # Если это диапазон
                    start, end = map(int, part.split('-'))
                    indices.extend(range(start, end + 1))
                elif part:  # Если это одиночный индекс
                    indices.append(int(part))
        except ValueError:
            raise ValueError("Некорректный формат диапазонов столбцов.")
        return list(dict.fromkeys(indices))  # Убираем дубликаты и сортируем

    def post(self, request, *args, **kwargs):
        # Получаем параметры из запроса
        file = request.FILES.get("file")
        column_range = request.data.get("column_range", "")
        num_rows = int(request.data.get("num_rows", 5))  # Количество строк (по умолчанию 5)
        header = request.data.get("header", "Column")

        if not file:
            return Response({"error": "Файл не предоставлен."}, status=400)

        if not column_range:
            return Response({"error": "Диапазон столбцов не указан."}, status=400)

        try:
            # Определяем тип файла и читаем его
            file_extension = file.name.split('.')[-1].lower()
            if file_extension in ['xls', 'xlsx']:
                df = pd.read_excel(file)
            elif file_extension == 'csv':
                df = pd.read_csv(file)
            else:
                return Response({"error": "Неподдерживаемый тип файла."}, status=400)

            # Парсим диапазон столбцов
            try:
                column_indices = self.parse_column_ranges(column_range)
            except ValueError as e:
                return Response({"error": str(e)}, status=400)

            # Проверяем, существуют ли указанные столбцы
            if any(idx < 0 or idx >= len(df.columns) for idx in column_indices):
                return Response({"error": "Некорректный индекс столбца."}, status=400)

            # Извлекаем и соединяем данные из указанных столбцов
            selected_columns = df.iloc[:, column_indices]
            selected_columns = (
                selected_columns
                .head(num_rows)
                .replace({np.nan: None})
                .astype(str)
                .apply(lambda row: " ".join(filter(None, row)), axis=1)
                .tolist()
            )

            result = {
                header: selected_columns
            }



            return Response(result, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
