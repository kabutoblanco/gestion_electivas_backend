from django.urls import path
from rest_framework_jwt.views import verify_jwt_token
from .views import *

urlpatterns = [
    # TOKENS
    path('api/verificate/', verify_jwt_token),
    # - - - - -
    # LOGIN
    path('api/login/', UserAccessAPI.as_view()),
    # - - - - -
    # SEMESTER
    path('api/semester/', SemesterAPI.as_view()),
    # - - - - -
    # FACULTY
    path('api/faculty/', FacultyAPI.as_view()),
    # - - - - -
    # CLASSROOM
    path('api/classroom/', ClassroomAPI.as_view()),
    path('api/getclassroom/<int:id>', ClassroomAPI.get_id),
    path('api/deleteclassroom/<int:id>', ClassroomAPI.delete),
    path('api/classroom/count/', ClassroomAPI.count),
    path('api/classroom/limit/<int:init>/<int:end>', ClassroomAPI.limit),
    # - - - - -
    # SCHEDULE
    path('api/schedule/', SchedulesAPI.as_view()),
    path('api/schedule/<int:id>', SchedulesAPI.get_id),
    # - - - - -
    # AVALIABLE_HOUR
    path('api/avaliable/', AvaliableHourAPI.as_view()),
    path('api/avaliable/get/<int:id>', AvaliableHourAPI.get),
    path('api/avaliable/<int:id>', AvaliableHourAPI.get_id),
    path('api/avaliable/course/<int:id>', CourseScheduleAPI.get_id),
    # - - - - -
    # STUDENT
    path('api/file/', StudentAPI.as_view()),
    path('api/enrrollment/', EnrrollmentAPI.as_view()),
    path('api/enrrollment/<int:id>/<int:semester>', EnrrollmentAPI.get_id),
    path('api/student/', StudentAPI.as_view()),
    path('api/student/update/', StudentAuxAPI.as_view()),
    path('api/student/<int:id>', StudentAPI.get_id),
    path('api/student/count/<int:id>', StudentAPI.count_id),
    path('api/student/delete/<int:id>', StudentAPI.delete),
    path('api/student/limit/<int:init>/<int:end>/<int:id>', StudentAPI.limit_id),
    # - - - - -
    # PROFESSOR
    path('api/professor/', ProfessorAPI.as_view()),
    # - - - - -
    # COURSE
    path('api/course/', CourseAPI.as_view()),
    path('api/course/delete/<int:id>', CourseAPI.delete),
    path('api/course/<int:id>', CourseAPI.get_id),
    path('api/course/semester/<int:id>', CourseAPI.get_semester),
    path('api/course/count/', CourseAPI.count),
    path('api/course/count/<int:id>', CourseAPI.count_id),
    path('api/course/limit/<int:init>/<int:end>', CourseAPI.limit),
    path('api/course/limit/<int:init>/<int:end>/<int:id>', CourseAPI.limit_id),
    # - - - - -
    # COURSE SCHEDULE
    path('api/course/schedule/', CourseScheduleAPI.as_view()),
    # - - - - -
    # ENRROLLMENT
    path('api/enrrollment/count/<int:id>/<str:user>', EnrrollmentAPI.count_id),
    path('api/enrrollment/limit/<int:init>/<int:end>/<int:id>/<str:user>', EnrrollmentAPI.limit_id),
    # - - - - -
]
