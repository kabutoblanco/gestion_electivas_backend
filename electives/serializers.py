from rest_framework import serializers
from .models import Secretary, Semester, Schedule, AvaliableHour, Classroom

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secretary
        fields = ('username',)
        
class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ('year', 'period', 'from_date', 'until_date', 'from_date_vote', 'until_date_vote')
        
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