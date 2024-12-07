from .models import Result
from .serializers import ResultSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from rest_framework.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from .parse_file import parse_file



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

