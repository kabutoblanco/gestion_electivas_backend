from django.urls import path
from rest_framework_jwt.views import verify_jwt_token
from .views import ClassroomGet, FacultyAPI, SecretaryLogin, ClassroomRegistration, StudentsUploadView, SemesterRegistration, SchedulesRegistration

urlpatterns = [
    path('api/verificate/', verify_jwt_token),
    path('api/login/', SecretaryLogin.as_view(), name="secretary-login"),
    path('api/semester/', SemesterRegistration.as_view(), name="semester-register"),
    path('api/schedule/', SchedulesRegistration.as_view(), name="schedules-register"),
    path('api/schedule/<int:id>', SchedulesRegistration.get, name="schedules-register"),
    path('api/classroom/', ClassroomRegistration.as_view(), name="classroom-register"),
    path('api/classroom/count/', ClassroomRegistration.count),
    path('api/classroom/limit/<int:init>/<int:end>', ClassroomRegistration.limit),
    path('api/getclassroom/<int:id>', ClassroomGet.get),
    path('api/faculty/', FacultyAPI.as_view(), name="faculty"),
    path('api/deleteclassroom/<int:id>', ClassroomRegistration.delete),
    path('api/file/', StudentsUploadView.as_view(), name="students-regiters"),
]