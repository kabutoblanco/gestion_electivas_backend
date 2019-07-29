from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count

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

from .serializers import *
from .models import Schedule, AvaliableHour, Classroom, Faculty
from django.core import serializers
from django.http import HttpResponse

# LOGIN


class UserAccessAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        queryset = User.objects.all().values('groups')
        print(queryset)
        if username is None or password is None:
            return Response({"error": "Ingrese usuario y constraseña"}, status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        serializer = UserSerializer(user, read_only=True, many=False)
        if not user:
            return Response({"error": "El usuario no existe"}, status=HTTP_404_NOT_FOUND)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({"user": serializer.data, "token": token}, status=HTTP_200_OK)
# - - - - -


class ProfessorAPI(APIView):
    permission_classes = (AllowAny,)

    # REQUESTS CRUD
    def get_id(self, id, format=None):
        pass

    def get(self, request, format=None):
        queryset = Professor.objects.all().values('id', 'first_name', 'last_name')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")


class SemesterAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SemesterSerializer

    # REQUESTS CRUD
    def post(self, request, format=None):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=False)
        serializer.save()
        queryset = self.serializer_class.items.all().filter(
            year=request.data.get("year"), period=request.data.get("period"))
        qs_json = serializers.serialize("json", queryset)
        return HttpResponse(qs_json, status=HTTP_201_CREATED)

    def get(self, format=None):
        queryset = self.serializer_class.items.all()
        qs_json = serializers.serialize("json", queryset)
        return HttpResponse(qs_json, content_type="application/json")
    # - - - - -


class FacultyAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = FacultySerializer

    # REQUESTS CRUD
    def post(self, request, format=None):
        queryset = self.serializer_class.items.all()
        qs_json = serializers.serialize(
            "json", queryset, fields=("id", "name"))
        return HttpResponse(qs_json, content_type="application/json")
    # - - - - -


class ClassroomAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ClassroomSerializer

    # REQUESTS CRUD
    def get_id(self, id, format=None):
        queryset = Classroom.objects.get(pk=id)
        queryset = serializers.serialize("json", [queryset])
        return HttpResponse(queryset, content_type="application/json")

    def get(self, request, format=None):
        queryset = Classroom.objects.all().values(
            "id", "classroom_id", "capacity", "faculty__name")
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    def post(self, request, format=None):
        id = request.data["id"]
        modelo = Classroom.objects.get(pk=id)
        modelo.classroom_id = request.data["classroom_id"]
        modelo.capacity = request.data["capacity"]
        modelo.faculty = Faculty.objects.get(pk=request.data["faculty"])
        modelo.description = request.data["description"]
        modelo.save()
        return Response(status=HTTP_200_OK)

    def put(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED)

    @csrf_exempt
    def delete(self, id, format=None):
        classroom = Classroom.objects.get(pk=id)
        classroom.delete()
        return HttpResponse(status=HTTP_200_OK)
    # - - - - -

    # OTHERS REQUESTS
    @csrf_exempt
    def limit(self, init, end, format=None):
        queryset = Classroom.objects.all()[init:end].values(
            "id", "classroom_id", "capacity", "faculty__name")
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    def count(self, format=None):
        count = Classroom.objects.all().count()
        return HttpResponse(count, status=HTTP_200_OK)
    # - - - - -


class SchedulesAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_schedule = ScheduleSerializer
    serializer_avaliable = AvaliableHourSerializer
    register = None

    # REQUESTS CRUD
    def get_id(self, id, format=None):
        queryset = AvaliableHour.objects.filter(classroom=id).values(
            "schedule", "schedule__time_from", "schedule__time_to", "schedule__day")
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    def post(self, request, format=None):
        schedules_delete = request.data["schedules_delete"]
        schedules_add = request.data["schedules_add"]
        classroom = request.data["id"]
        for schedule_delete in schedules_delete:
            q1 = AvaliableHour.objects.filter(schedule=schedule_delete.get(
                "schedule"), classroom=classroom).first()
            q1.delete()
        for schedule_add in schedules_add:
            serializer = self.serializer_schedule(data=schedule_add)
            if (serializer.is_valid(raise_exception=False)):
                register = serializer.save()
                object_avaliable = {"classroom": int(
                    classroom), "schedule": register.id}
            else:
                register = Schedule.objects.filter(
                    time_from=schedule_add["time_from"], time_to=schedule_add["time_to"], day=schedule_add["day"])
                object_avaliable = {"classroom": int(
                    classroom), "schedule": register.first().id}
            print(register)
            json_avaliable = json.dumps(object_avaliable)
            json_avaliable = json.loads(json_avaliable)
            serializer = self.serializer_avaliable(data=json_avaliable)
            if (serializer.is_valid(raise_exception=False)):
                serializer.save()
        return Response(status=HTTP_201_CREATED)

    def put(self, request, format=None):
        classroom = request.data["classroom"]
        schedules = request.data["schedules"]
        classroom = Classroom.objects.filter(classroom_id=classroom).first().id
        for schedule in schedules:
            serializer = self.serializer_schedule(data=schedule)
            if (serializer.is_valid(raise_exception=False)):
                register = serializer.save()
                object_avaliable = {
                    "classroom": int(classroom), "schedule": register.id}
            else:
                register = Schedule.objects.filter(
                    time_from=schedule["time_from"], time_to=schedule["time_to"], day=schedule["day"])
                object_avaliable = {"classroom": int(
                    classroom), "schedule": register.first().id}
            json_avaliable = json.dumps(object_avaliable)
            json_avaliable = json.loads(json_avaliable)
            serializer = self.serializer_avaliable(data=json_avaliable)
            if (serializer.is_valid(raise_exception=False)):
                serializer.save()
        return Response(status=HTTP_201_CREATED)
    # - - - - -


class EnrrollmentAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = EnrrollmentSerializer

    @csrf_exempt
    def get_id(self, id, semester, format=None):
        queryset = Enrrollment.objects.filter(student__id=id, course__semester__id=semester).values(
            'course__id', 'course__course__name', 'course__professor__first_name', 'course__professor__last_name')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    def put(self, request, format=None):
        student = request.data["student"]
        enrrollments = request.data["enrrollments"]
        id_student = Student.objects.get(user_id=student).id
        for enrrollment in enrrollments:
            object_enrrollment = {"student": id_student,
                                  "course": enrrollment.get("id")}
            json_enrrollment = json.dumps(object_enrrollment)
            json_enrrollment = json.loads(json_enrrollment)
            serializer = self.serializer_class(data=json_enrrollment)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
        return Response(status=HTTP_201_CREATED)
    
    def post(self, request, format=None):
        enrrollments_delete = request.data["enrrollments_delete"]
        enrrollments_add = request.data["enrrollments_add"]
        student = request.data["student"]
        for enrrollment_delete in enrrollments_delete:
            print(enrrollment_delete.get(
                "course__id"))
            print(student)
            q1 = Enrrollment.objects.filter(course=enrrollment_delete.get(
                "course__id"), student=Student.objects.get(user_id=student).id)
            print(q1)
            q1.delete()
        for enrrollment in enrrollments_add:
            object_enrrollment = {"student": Student.objects.get(user_id=student).id,
                                  "course": enrrollment.get("course__id")}
            json_enrrollment = json.dumps(object_enrrollment)
            json_enrrollment = json.loads(json_enrrollment)
            serializer = self.serializer_class(data=json_enrrollment)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
        return Response(status=HTTP_201_CREATED)


class StudentAuxAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_student = StudentSerializer
    
    def post(self, request, format=None):
        print(request)
        id = request.data["id"]
        modelo = Student.objects.get(pk=id)
        modelo.user_id = request.data["user_id"]
        modelo.first_name = request.data["first_name"]
        modelo.last_name = request.data["last_name"]
        modelo.username = request.data["username"]
        modelo.email = request.data["username"] + "@unicauca.edu.co"
        modelo.save()
        return Response(status=HTTP_200_OK)

class StudentAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_student = StudentSerializer
    serializer_enrrollment = EnrrollmentSerializer

    def get(self, request, format=None):
        queryset = Student.objects.all().values(
            'id', 'user_id', 'first_name', 'last_name')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    @csrf_exempt
    def get_id(self, id, format=None):
        queryset = Student.objects.filter(id=id).values(
            'id', 'user_id', 'first_name', 'last_name', 'username')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    def put(self, request, format=None):
        serializer = self.serializer_student(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED)

    # OTHERS REQUESTS
    @csrf_exempt
    def limit_id(self, init, end, id, format=None):
        queryset = Enrrollment.objects.filter(course__semester=id)[init:end].values(
            'student__id', 'student__user_id', 'student__first_name', 'student__last_name').annotate(Count('student__id'))
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    def count_id(self, id, format=None):
        count = Enrrollment.objects.filter(course__semester=id).values(
            'student__id').annotate(Count('student__id')).count()
        return HttpResponse(count, status=HTTP_200_OK)
    # - - - - -

    def post(self, request, format=None):
        csv_file = request.FILES["csv_file"]
        semester = request.data['semester']
        if not csv_file.name.endswith(".csv"):
            return HttpResponse(status=HTTP_400_BAD_REQUEST)
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        response = "Errores en las filas:\n"
        i = 0
        for line in lines:
            if (line):
                fields = line.split(",")
                object_student = {
                    "user_id": fields[0], "username": fields[3], "first_name": fields[1], "last_name": fields[2],  "password": 'ninguna'}
                json_student = json.dumps(object_student)
                json_student = json.loads(json_student)
                serializer = self.serializer_student(data=json_student)

                if (serializer.is_valid(raise_exception=False)):
                    print('okkk')
                    serializer.save()
                else:
                    response = response + \
                        "\tFila (estudiante): " + str(i) + "\n"
                # FIND STUDENT

                student = Student.objects.filter(
                    user_id=json_student.get('user_id')).first().id
                # - - - - -
                # FIND COURSE
                course = CourseDetail.objects.filter(
                    course__course_id=fields[4], semester_id=semester).first().id
                print(course)
                # - - - - -
                object_enrrollment = {"student": student, "course": course}
                json_enrrollment = json.dumps(object_enrrollment)
                json_enrrollment = json.loads(json_enrrollment)
                serializer = self.serializer_enrrollment(data=json_enrrollment)
                if (serializer.is_valid(raise_exception=False)):
                    serializer.save()
                else:
                    response = response + "\tFila (curso): " + str(i) + "\n"
                i = i + 1
        return HttpResponse({response}, status=HTTP_200_OK)

    @csrf_exempt
    def delete(self, id, format=None):
        student = Student.objects.get(pk=id)
        student.delete()
        return HttpResponse(status=HTTP_200_OK)


class CourseAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CourseSerializer

    # REQUESTS CRUD
    def get_id(self, id, format=None):
        queryset = CourseDetail.objects.filter(id=id).values(
            'course__id', 'course__course_id', 'professor__id', 'quota', 'priority', 'from_date_vote', 'until_date_vote')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    @csrf_exempt
    def get_semester(self, id, format=None):
        queryset = CourseDetail.objects.filter(semester=id).values(
            'id', 'course__id', 'course__course_id', 'course__name', 'professor__first_name', 'professor__last_name')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    def get(self, request, format=None):
        queryset = CourseDetail.objects.all().values('id', 'course__id', 'course__course_id',
                                                     'course__name', 'professor__first_name', 'professor__last_name')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    def put(self, request, format=None):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            serializer.save()
        return Response(status=HTTP_201_CREATED)

    def post(self, request, format=None):
        id = request.data["id"]
        modelo = CourseDetail.objects.get(pk=id)
        modelo.quota = request.data["quota"]
        modelo.priority = request.data["priority"]
        modelo.from_date_vote = request.data["from_date_vote"]
        modelo.until_date_vote = request.data["until_date_vote"]
        modelo.professor = Professor.objects.get(id=request.data["professor"])
        modelo.course = Course.objects.get(id=request.data["course"])
        modelo.save()
        return Response(status=HTTP_200_OK)

    @csrf_exempt
    def delete(self, id, format=None):
        course = CourseDetail.objects.get(pk=id)
        course.delete()
        return HttpResponse(status=HTTP_200_OK)
    # - - - - -

    # OTHERS REQUESTS
    @csrf_exempt
    def limit(self, init, end, format=None):
        queryset = CourseDetail.objects.all()[init:end].values(
            'id', 'course__id', 'course__course_id', 'course__name', 'professor__first_name', 'professor__last_name')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    @csrf_exempt
    def limit_id(self, init, end, id, format=None):
        queryset = CourseDetail.objects.filter(semester=id)[init:end].values(
            'id', 'course__id', 'course__course_id', 'course__name', 'professor__first_name', 'professor__last_name')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    def count(self, format=None):
        count = CourseDetail.objects.all().count()
        return HttpResponse(count, status=HTTP_200_OK)

    def count_id(self, id, format=None):
        count = CourseDetail.objects.filter(semester=id).count()
        return HttpResponse(count, status=HTTP_200_OK)
    # - - - - -


class AvaliableHourAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AvaliableHourSerializer

    # REQUESTS CRUD
    @csrf_exempt
    def get_id(self, id, format=None):
        queryset = AvaliableHour.objects.filter(classroom=id).values(
            'id', 'schedule__id', 'schedule__day', 'schedule__time_from', 'schedule__time_to')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    @csrf_exempt
    def get(self, id, format=None):
        queryset = AvaliableHour.objects.filter(id=id).values(
            'id', 'schedule__id', 'schedule__day', 'schedule__time_from', 'schedule__time_to')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    # OTHERS REQUESTS
    @csrf_exempt
    def limit(self, init, end, format=None):
        queryset = CourseDetail.objects.all()[init:end].values(
            'id', 'course__id', 'course__course_id', 'course__name', 'professor__first_name', 'professor__last_name')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    @csrf_exempt
    def limit_id(self, init, end, id, format=None):
        queryset = CourseDetail.objects.filter(semester=id)[init:end].values(
            'id', 'course__id', 'course__course_id', 'course__name', 'professor__first_name', 'professor__last_name')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    def count(self, format=None):
        count = CourseDetail.objects.all().count()
        return HttpResponse(count, status=HTTP_200_OK)

    def count_id(self, id, format=None):
        count = CourseDetail.objects.filter(semester=id).count()
        return HttpResponse(count, status=HTTP_200_OK)
    # - - - - -


class CourseScheduleAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CourseScheduleSerializer

    # REQUESTS CRUD
    @csrf_exempt
    def get_id(self, id, format=None):
        queryset = CourseSchedule.objects.filter(course=id).values(
            'id', 'avaliable__schedule__id', 'avaliable__schedule__day', 'avaliable__schedule__time_from', 'avaliable__schedule__time_to')
        queryset = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(queryset, content_type="application/json")

    def put(self, request, format=None):
        course = request.data["course"]
        schedules = request.data["schedules"]
        for schedule in schedules:
            object_avaliable = {
                "avaliable": schedule.get('id'), "course": course}
            json_avaliable = json.dumps(object_avaliable)
            json_avaliable = json.loads(json_avaliable)
            serializer = self.serializer_class(data=json_avaliable)
            if (serializer.is_valid(raise_exception=False)):
                register = serializer.save()
        return Response(status=HTTP_201_CREATED)

    def post(self, request, format=None):
        schedules_delete = request.data["avaliable_hours_delete"]
        schedules_add = request.data["avaliable_hours_add"]
        course = request.data["id"]
        print(schedules_add)
        for schedule_delete in schedules_delete:
            q1 = CourseSchedule.objects.get(id=schedule_delete.get("id"))
            q1.delete()
        for schedule_add in schedules_add:
            serializer = self.serializer_class(data=schedule_add)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
        return Response(status=HTTP_201_CREATED)
