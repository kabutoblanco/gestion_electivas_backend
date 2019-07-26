from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secretary
        fields = ('username',)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('user_id', 'username', 'first_name', 'last_name', 'password')
    
    items = Student.objects
    
    def create(self, validated_data):
        return Student.objects.create_student(**validated_data)
    
class EnrrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrrollment
        fields = ('student', 'course')
    
    items = Enrrollment.objects
    
    def create(self, validated_data):
        return Enrrollment.objects.create_enrrollment(**validated_data)

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ('year', 'period', 'from_date', 'until_date')

    items = Semester.objects

    def create(self, validated_data):
        return Semester.objects.create_semester(**validated_data)


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('time_from', 'time_to', 'day')

    def create(self, validated_data):
        return Schedule.objects.create_schedule(**validated_data)


class AvaliableHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvaliableHour
        fields = ('classroom', 'schedule')

    def create(self, validated_data):
        return AvaliableHour.objects.create_hour(**validated_data)


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ('classroom_id', 'capacity', 'description', 'faculty')

    def create(self, validated_data):
        return Classroom.objects.create_classroom(**validated_data)

    items = Classroom.objects


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('classroom_id', 'capacity', 'description', 'faculty')

    items = Faculty.objects
    
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetail
        fields = ('classroom_id', 'capacity', 'description', 'faculty')

    def create(self, validated_data):
        return CourseDetail.objects.create_classroom(**validated_data)

    items = Classroom.objects

