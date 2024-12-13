import datetime
from django.core.paginator import Paginator
from .models import SportType, Discipline, ContestType, AgeGroup, Contest, ContestDiscipline, ContestAgeGroup
from .serializers import SportTypeSerializer, DisciplineSerializer, ContestTypeSerializer, AgeGroupSerializer, ContestSerializer, ContestDisciplineSerializer, ContestAgeGroupSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils import get_page_object


# Create your views here.

class SportTypeView(ModelViewSet):
    #permission_classes = [IsAuthenticated]

    queryset = SportType.objects.all()
    serializer_class = SportTypeSerializer
    

class DisciplineView(ModelViewSet):
    #permission_classes = [IsAuthenticated]

    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer

    def get_disciplines_by_sport_type(self, request, sport_type_id=None):
        ids = request.GET.getlist('sporttype')
        disciplines = Discipline.objects.filter(sport_type_id__in=ids)
        serializer = self.get_serializer(disciplines, many=True)
        return Response(serializer.data, status=200)

class ContestTypeView(ModelViewSet):
    #permission_classes = [IsAuthenticated]

    queryset = ContestType.objects.all()
    serializer_class = ContestTypeSerializer

class AgeGroupView(ModelViewSet):
    #permission_classes = [IsAuthenticated]

    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer


class ContestView(ModelViewSet):
    #permission_classes = [IsAuthenticated]

    queryset = Contest.objects.all()
    serializer_class = ContestSerializer

    def get_contest_discpilines_ages(self, contests):
        disciplines = {}
        age_group = {}
        sport_types = {}
        for contest in contests:
            disciplines[contest.id] = []
            age_group[contest.id] = []
            ds = ContestDiscipline.objects.filter(contest__id=contest.id)
            for d in ds:
                disciplines[contest.id].append(d.discipline.name)
            ages = ContestAgeGroup.objects.filter(contest__id=contest.id)
            for a in ages:
                age_group[contest.id].append(str(a.age_group))
            sport_types[contest.id] = str(ds[0].discipline.sport_type)
        return disciplines, age_group, sport_types

    def retrieve(self, request, *args, **kwargs):
        # do your customization here
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        disciplines, age_group, sport_types = self.get_contest_discpilines_ages([instance])
        return Response({'data': {'contest': serializer.data, 'disciplines': disciplines, 'age_group': age_group, 'sport_types': sport_types}}, status=200)
    
    def list(self, request, *args, **kwargs):
        try:
            page = int(request.GET['page'])
            per_page = int(request.GET['per_page'])
        except:
            page = 1
            per_page = 10
        objs, page, per_page, total = get_page_object(self.queryset.order_by('id'), page, per_page)

        disciplines, ages, sport_types = self.get_contest_discpilines_ages(objs)

        ser = self.get_serializer(objs, many=True)
        return Response({'data': {'contests': ser.data, 'disciplines':disciplines, 'ages':ages, 'sport_types': sport_types}, 'pages':{"total": total, "per_page": per_page, 'cur_page': page}}, status=200)

    def get_filter_data(self, request):
        
        if 'sporttype' in request.GET:
            self.queryset = self.queryset.filter(contestdiscipline__discipline__sport_type__id__in=request.GET.getlist('sporttype')).distinct()
        if 'discipline' in request.GET:
            self.queryset = self.queryset.filter(contestdiscipline__discipline__id__in=request.GET.getlist('discipline')).distinct()
        if 'contesttype' in request.GET:
            self.queryset = self.queryset.filter(contest_type__id__in=request.GET.getlist('contesttype'))
        #if 'agestart' in request.GET:
        #    self.queryset = self.queryset.filter(contestagegroup__age_group__start__gte=request.GET['agestart']).distinct()
        #if 'ageend' in request.GET:
        #    self.queryset = self.queryset.filter(contestagegroup__age_group__end__lte=request.GET['ageend']).distinct()
        #if 'gender' in request.GET:
        #    self.queryset = self.queryset.filter(contestagegroup__age_group__gender=request.GET['gender']).distinct()
        if 'agegroup' in request.GET:
            self.queryset = self.queryset.filter(contestagegroup_age_group__id__in=request.GET.getlist('agegroup'))
        if 'starttime' in request.GET:
            print('starttime')
            try:
                print(request.GET['starttime'])
                start = datetime.datetime.strptime(request.GET['starttime'], '%d-%m-%Y')
                self.queryset = self.queryset.filter(start_time__gte=start)
            except Exception as e:
                print(e)
                return Response({'error': 'Формат даты начала периода задан неверно!'}, status=404)
        if 'endtime' in request.GET:
            print('endtime')
            try:
                print(request.GET['endtime'])
                end = datetime.datetime.strptime(request.GET['endtime'], '%d-%m-%Y')
                self.queryset = self.queryset.filter(end_time__lte=end)
            except:
                return Response({'error': 'Формат даты конца периода задан неверно!'}, status=404)
        if 'place' in request.GET:
            #self.queryset = self.queryset.filter(organizer__region__id=request.GET['region'])
            self.queryset = self.queryset.filter(place__icontains=request.GET['region'])


        try:
            page = int(request.GET['page'])
            per_page = int(request.GET['per_page'])
        except:
            page = 1
            per_page = 10
        objs, page, per_page, total = get_page_object(self.queryset.order_by('id'), page, per_page)
        
        disciplines, ages, sport_types = self.get_contest_discpilines_ages(objs)

        ser = self.get_serializer(objs, many=True)
        return Response({'data': {'contests': ser.data, 'disciplines':disciplines, 'ages':ages, 'sport_types': sport_types}, 'pages':{"total": total, "per_page": per_page, 'cur_page': page}}, status=200)


class ContestDisciplineView(ModelViewSet):
    
    queryset = ContestDiscipline.objects.all()
    serializer_class = ContestDisciplineSerializer


class ContestAgeGroupView(ModelViewSet):
    
    queryset = ContestAgeGroup.objects.all()
    serializer_class = ContestAgeGroupSerializer
