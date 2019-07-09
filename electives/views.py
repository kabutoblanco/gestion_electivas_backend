from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import json

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings

from .serializers import UserSerializer, ClassroomSerializer, SemesterSerializer, ScheduleSerializer, AvaliableHourSerializer
from .models import Schedule, AvaliableHour

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

# 1er HU: Work 3
class ClassroomRegistration(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ClassroomSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED)

class SchedulesRegistration(APIView):
    permission_classes = (AllowAny,)
    serializer_schedule = ScheduleSerializer
    serializer_avaliable = AvaliableHourSerializer
    register = None
    def post(self, request, format=None):
        classroom = request.data["classroom"]
        schedules = request.data["schedules"]
        for schedule in schedules:
            serializer = self.serializer_schedule(data=schedule)
            if (serializer.is_valid(raise_exception=False)):
                register = serializer.save()
            else:
                register = Schedule.objects.filter(time_from=schedule['time_from'], time_to=schedule['time_to'], day=schedule['day'])
            object_avaliable = {"classroom": int(classroom), "schedule":register.first().id}
            json_avaliable = json.dumps(object_avaliable)
            json_avaliable = json.loads(json_avaliable)
            serializer = self.serializer_avaliable(data=json_avaliable)
            if (serializer.is_valid(raise_exception=False)):
                serializer.save()
        return Response(status=HTTP_201_CREATED)

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