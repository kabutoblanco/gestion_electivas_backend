from django.urls import path
from rest_framework_jwt.views import verify_jwt_token, refresh_jwt_token
from .views import *

urlpatterns = [
    # TOKENS
    path('api/verificate/', verify_jwt_token),
    path('api/refresh/', refresh_jwt_token),
    # - - - - -
    # LOGIN
    path('api/login/', UserAccessAPI.as_view()),
    # - - - - -
    # SEMESTER
    path('api/semester/', SemesterAPI.as_view()),
    path('api/semester/<int:id>', SemesterAPI.get_id),
    # - - - - -
    # FACULTY
    path('api/faculty/', FacultyAPI.as_view()),
    # - - - - -
    # CLASSROOM
    path('api/classroom/', ClassroomAPI.as_view()),
    path('api/getcourse/<int:course>', ClassroomAPI.get_course),
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
    path('api/avaliable/profeesor_get/<int:id>', AvaliableHourAPI.get_professor_id),
    path('api/avaliable/profeesor_schedule/<int:id>', AvaliableHourAPI.get_professor_schedule),
    path('api/avaliable/professor/<int:id>/<int:course>', AvaliableHourAPI.get_professor),
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
    path('api/course/all', CourseAPI.get_all),
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
    path('api/course/schedule/professor/<int:id>', CourseScheduleProfessorAPI.get_id),
    path('api/course/schedule/professor/<int:avaliable>/<int:course>', CourseScheduleProfessorAPI.get_schedules),
    path('api/course/avaliable/<int:elective>', CourseScheduleProfessorAPI.myschedule_electives),
    path('api/course/scheduleprofessor/<str:professor>/<int:elective>', CourseScheduleProfessorAPI.myavalible_electives),
    # - - - - -
    # ENRROLLMENT
    path('api/enrrollment/count/<int:id>/<str:user>', EnrrollmentAPI.count_id),
    path('api/enrrollment/limit/<int:init>/<int:end>/<int:id>/<str:user>', EnrrollmentAPI.limit_id),
    # - - - - -
    # STUDENT VOTE
    path('api/student/vote/', CourseScheduleStudentAPI.as_view()),
    path('api/student/vote/<int:id>/<str:student>', CourseScheduleStudentAPI.get_id),
    # - - - - -
    # COURSE PROFESSOR
    path('api/course/professor/', CourseScheduleProfessorAPI.as_view()),
    path('api/course/professor/limit/<int:init>/<int:end>/<int:semester>/<str:professor>', CourseScheduleProfessorAPI.limit_electives),
    path('api/course/professor/count/<int:semester>/<str:professor>', CourseScheduleProfessorAPI.count_electives),
    # - - - - -
]
