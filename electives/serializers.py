from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'groups')

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
        fields = ('quota',
                'priority',
                "from_date_vote",
                "until_date_vote",
                "course",
                "professor",
                "semester")

    def create(self, validated_data):
        return CourseDetail.objects.create_course(**validated_data)

    items = CourseDetail.objects
    
class CourseScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSchedule
        fields = ('avaliable', 'course')

    def create(self, validated_data):
        return CourseSchedule.objects.create_schedule(**validated_data)
    
class StudentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentVote
        fields = ('student', 'schedule')
    
    def create(self, validated_data):
        return StudentVote.objects.create_studentvote(**validated_data)
    
class ProfessorVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorVote
        fields = ('professor', 'schedule')
    
    def create(self, validated_data):
        return ProfessorVote.objects.create_professorvote(**validated_data)

