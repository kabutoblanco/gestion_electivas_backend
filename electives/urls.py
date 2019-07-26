from django.urls import path
from rest_framework_jwt.views import verify_jwt_token
from .views import *

urlpatterns = [
    # TOKENS
    path('api/verificate/', verify_jwt_token),
    # - - - - -
    # LOGIN
    path('api/login/', SecretaryAccessAPI.as_view()),
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
    path('api/avaliable/<int:id>', AvaliableHourAPI.get_id),
    # - - - - -
    # STUDENT
    path('api/file/', StudentAPI.as_view()),
    # - - - - -
    # COURSE
    path('api/course/', CourseAPI.as_view()),
    path('api/course/count/', CourseAPI.count),
    path('api/course/count/<int:id>', CourseAPI.count_id),
    path('api/course/limit/<int:init>/<int:end>', CourseAPI.limit),
    path('api/course/limit/<int:init>/<int:end>/<int:id>', CourseAPI.limit_id),
    # - - - - -
]
