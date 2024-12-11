from django.utils.dateparse import parse_date
from .models import Result, ResultFile
from country.models import Region
from contests.models import Contest
from contestant.models import Team
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
from fsp.settings import *
import boto3

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

class FSResultsView(ModelViewSet):  
    queryset = Result.objects.all()
    regions = Region.objects.all()
    serializer_class = ResultSerializer
    
    def get_queryset(self):
        contest_id = self.request.query_params.get('contest', None)
        region_id = self.request.query_params.get('region', None)
        date_str = self.request.query_params.get('date', None)

        results = self.queryset
        filters = {}

        if contest_id:
            filters['contest__id'] = contest_id
        if region_id:
            filters['contest__federation__region__id'] = region_id
        if date_str:
            date = parse_date(date_str)
            if not date:
                raise ValidationError('Неверный формат даты. Ожидается YYYY-MM-DD.')
            filters['contest__start_time__date'] = date

        if filters:
            results = results.filter(**filters)
        
        return results

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True) 
        return Response(serializer.data, status=HTTP_200_OK)

    def search(self, request):
        results = self.queryset
        region = self.request.query_params.get('region', None)
        search_result = []

        for result in results:
            if result.sender_federation and result.sender_federation.region:
                if result.sender_federation.region.name and \
                    region.lower() in result.contest.organizer.region.name.lower():
                    search_result.append(result)
        
        serializer = self.get_serializer(search_result, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
     

class ColumnPreviewAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def parse_column_ranges(self, column_range: str) -> list:
        """
        Парсит строку с диапазонами столбцов и возвращает список индексов.
        Пример входных данных: "3, 5, 6-12, , 312"
        Индексация столбцов в пользовательском вводе начинается с 1, а в DataFrame — с 0.
        """
        indices = []
        try:
            for part in column_range.split(','):
                part = part.strip()
                if '-' in part:  # Если это диапазон
                    start, end = map(int, part.split('-'))
                    indices.extend(range(start - 1, end))  # Преобразуем в 0-based индексы
                elif part:  # Если это одиночный индекс
                    indices.append(int(part) - 1)  # Преобразуем в 0-based индекс
        except ValueError:
            raise ValueError("Некорректный формат диапазонов столбцов.")
        return list(dict.fromkeys(indices))  # Убираем дубликаты, сохраняя порядок

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
        
class ResultUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def parse_range(self, range_str: str) -> list:
        """
        Парсит строку диапазонов в список индексов.
        Пример: "4-5" -> [4, 5]
        """
        indices = []
        for part in range_str.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                indices.extend(range(start, end + 1))
            elif part.isdigit():
                indices.append(int(part))
        return indices

    def post(self, request, *args, **kwargs):
        # Получаем файл и данные из запроса
        file = request.FILES.get("file")
        contest_id = request.data.get("contest_id")
        district_col = request.data.get("district", "").strip()
        region_col = request.data.get("region", "").strip()
        participants_col = request.data.get("participants", "").strip()
        points_col = request.data.get("points", "").strip()
        place_col = request.data.get("place", "").strip()

        if not file:
            return Response({"error": "Файл не предоставлен."}, status=400)

        if not contest_id:
            return Response({"error": "ID соревнования не предоставлен."}, status=400)

        try:
            # Получаем конкурс
            contest = Contest.objects.get(id=contest_id)

            # Определяем тип файла и читаем его
            file_extension = file.name.split('.')[-1].lower()
            if file_extension in ['xls', 'xlsx']:
                df = pd.read_excel(file)
            elif file_extension == 'csv':
                df = pd.read_csv(file)
            else:
                return Response({"error": "Неподдерживаемый тип файла."}, status=400)

            # Парсинг столбцов
            contest = Contest.objects.filter(id=contest_id).first()

            parsed_data = {}
            for i, row in df.iterrows():
                # Используем iloc для доступа по позиции
                district = row.iloc[int(district_col)] if district_col.isdigit() else None
                region = row.iloc[int(region_col)] if region_col.isdigit() else None
                participants_indices = self.parse_range(participants_col)
                participants = " ".join([str(row.iloc[idx]) for idx in participants_indices if idx < len(row)])

                # Проверка и обработка points
                points = row.iloc[int(points_col)] if points_col.isdigit() else None
                if points is not None and not pd.isna(points):
                    try:
                        points = int(float(points))  # Обрабатываем, если это строка с числом
                    except ValueError:
                        points = None  # Если значение не числовое, заменяем его на None

                # Проверка и обработка place
                place = row.iloc[int(place_col)] if place_col.isdigit() else None
                if place is not None and not pd.isna(place):
                    try:
                        place = int(float(place))  # Обрабатываем, если это строка с числом
                    except ValueError:
                        place = None  # Если значение не числовое, заменяем его на None

                # Сохраняем результат только если points и place валидны
                if points is not None and participants is not None:
                    parsed_data['name'] = 'Команда1'
                    parsed_data['team'] = participants
                    parsed_data['score'] = points

                    r = Region.objects.get(id=1)
                    t = Team.objects.create(name=participants, members=participants, region=r)
                    r = Result.objects.create(contest=contest, team=t, score=points)
                    print(r)

            # Сохраняем все результаты через bulk_create
            # Result.objects.bulk_create(parsed_data)

            # Загружаем файл в S3
            s3 = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                endpoint_url=AWS_S3_ENDPOINT_URL
            )

            s3_file_name = f"results/{file.name}"
            s3.upload_fileobj(file, AWS_STORAGE_BUCKET_NAME, s3_file_name)

            # Сохраняем информацию о загруженном файле
            # result_file = ResultFile.objects.create(
            #     contest=contest,
            #     file=f"https://{AWS_S3_ENDPOINT_URL}/{s3_file_name}",
            #     results_protocol=True
            # )

            contest.file = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/{s3_file_name}"
            contest.save()

            return Response(
                {
                    "message": "Результаты успешно обработаны.",
                    "file_url": contest.file,
                },
                status=200,
            )

        except Contest.DoesNotExist:
            return Response({"error": "Соревнование не найдено."}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
