from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.core.serializers.json import DjangoJSONEncoder

import json

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from django.views.decorators.csrf import csrf_exempt

from .serializers import FacultySerializer, UserSerializer, ClassroomSerializer, SemesterSerializer, ScheduleSerializer, AvaliableHourSerializer
from .models import Schedule, AvaliableHour, Classroom, Faculty
from django.core import serializers
from django.http import HttpResponse

# Create your views here.
# 1er HU: Work 1
class SecretaryLogin(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        serializer = UserSerializer(user, read_only=True, many=False)
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'user': serializer.data, 'token': token}, status=HTTP_200_OK)

# 1er HU: Work 2
class SemesterRegistration(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SemesterSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED)

class FacultyAPI(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FacultySerializer
    def post(self, request, format=None):
        queryset = self.serializer_class.items.all()
        qs_json = serializers.serialize('json', queryset, fields=('id', 'name'))
        return HttpResponse(qs_json, content_type='application/json')

# 1er HU: Work 3
class ClassroomRegistration(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ClassroomSerializer
    def get(self, request, format=None):
        queryset = self.serializer_class.items.all()
        qs_json = serializers.serialize('json', queryset, fields=('id', 'classroom_id', 'capacity'))
        return HttpResponse(qs_json, content_type='application/json')  
    def put(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED)
    def post(self, request, format=None):
        print(request.data["id"])
        id = request.data["id"]
        modelo = Classroom.objects.get(pk=id)
        modelo.classroom_id = request.data["classroom_id"]
        modelo.capacity = request.data["capacity"]
        modelo.faculty = Faculty.objects.get(pk=request.data["faculty"])
        modelo.description = request.data["description"]
        modelo.save()
        return Response(status=HTTP_200_OK)
    @csrf_exempt
    # csrf temporal
    def delete(self, id, format=None):
        classroom = Classroom.objects.get(pk=id)
        classroom.delete()
        return HttpResponse(status=HTTP_200_OK)

class ClassroomGet(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ClassroomSerializer
    def get(self, id, format=None):
        queryset = Classroom.objects.get(pk=id)
        queryset = serializers.serialize('json', [queryset]);
        return HttpResponse(queryset, content_type='application/json')  

class SchedulesRegistration(APIView):
    permission_classes = (AllowAny,)
    serializer_schedule = ScheduleSerializer
    serializer_avaliable = AvaliableHourSerializer
    register = None    
    def get(self, id, format=None):
        queryset = AvaliableHour.objects.filter(classroom=id).values('schedule', 'schedule__time_from', 'schedule__time_to', 'schedule__day')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)   
        return HttpResponse(queryset, content_type='application/json')  
    def put(self, request, format=None):
        print('avaliable hours')
        classroom = request.data["classroom"]
        schedules = request.data["schedules"]
        classroom = Classroom.objects.filter(classroom_id=classroom).first().id
        for schedule in schedules:
            serializer = self.serializer_schedule(data=schedule)
            if (serializer.is_valid(raise_exception=False)):
                register = serializer.save()
                object_avaliable = {"classroom": int(classroom), "schedule": register.id}            
            else:                
                register = Schedule.objects.filter(time_from=schedule["time_from"], time_to=schedule["time_to"], day=schedule["day"])
                object_avaliable = {"classroom": int(classroom), "schedule": register.first().id}   
            print(register)         
            json_avaliable = json.dumps(object_avaliable)
            json_avaliable = json.loads(json_avaliable)
            serializer = self.serializer_avaliable(data=json_avaliable)
            if (serializer.is_valid(raise_exception=False)):
                print("ok") 
                serializer.save()
            else:
                print("fallo") 
        return Response(status=HTTP_201_CREATED)
    def post(self, request, format=None):
        schedules = request.data["schedules"]

#TODO
class StudentsUploadView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            return Response(status=HTTP_400_BAD_REQUEST)
        file_data = csv_file.read().decode("utf-8")	
        lines = file_data.split("\n")
        for line in lines:				
            fields = line.split(",")
            if fields[0]:
                print(fields[0])
        return Response(status=HTTP_200_OK)