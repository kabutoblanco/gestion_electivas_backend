from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import send_mail

# Create your models here.


class User(AbstractUser):
    user_id = models.IntegerField(default=0, unique=True)
    username = models.CharField(
        max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_('password'), max_length=128)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']

    def __str__(self):
        return "{}".format(self.username)


# Manager models
class SecretaryManager(BaseUserManager):
    def create_secretary(self, user_id, first_name, last_name, username, password):
        email = username + "@unicauca.edu.co"
        secretary = Secretary(user_id=user_id, username=username, first_name=first_name, last_name=last_name,
                              email=self.normalize_email(email),)
        secretary.set_password(password)
        secretary.save()
        secretary.groups.add(Group.objects.get(name='secretary'))
        return secretary


class ProfessorManager(BaseUserManager):
    def create_professor(self, user_id, first_name, last_name, username, password):
        email = username + "@unicauca.edu.co"
        proffesor = Professor(user_id=user_id, username=username, first_name=first_name, last_name=last_name,
                              email=self.normalize_email(email),)
        proffesor.set_password(password)
        proffesor.save()
        student.groups.add(Group.objects.get(name='professor'))
        return proffesor


class StudentManager(BaseUserManager):
    def create_student(self, user_id, first_name, last_name, username, password):
        email = username + "@unicauca.edu.co"
        student = Student(user_id=user_id, username=username, first_name=first_name, last_name=last_name,
                          email=self.normalize_email(email),)
        student.set_password(password)
        student.save()
        # send_mail(
        #     'Registro en la plataforma SGE Unicauca',
        #     'El estudiante ha sido registrado en la plataforma SGE para poder votar las electivas matriculadas',
        #     'mdquilindo@unicauca.edu.co',
        #     [email],
        #     fail_silently=False,
        # )
        student.groups.add(Group.objects.get(name='student'))
        return student


class SemesterManager(BaseUserManager):
    def create_semester(self, year, period, from_date, until_date):
        semester = Semester(year=year,
                            period=period,
                            from_date=from_date,
                            until_date=until_date,)
        semester.save()
        return semester


class ScheduleManager(BaseUserManager):
    def create_schedule(self, time_from, time_to, day):
        schedule = Schedule(time_from=time_from, time_to=time_to, day=day)
        schedule.save()
        return schedule


class AvaliableHourManager(BaseUserManager):
    def create_hour(self, classroom, schedule):
        hour = AvaliableHour(classroom=classroom, schedule=schedule)
        hour.save()
        return hour


class ClassroomManager(BaseUserManager):
    def create_classroom(self, classroom_id, capacity, description, faculty):
        classroom = Classroom(classroom_id=classroom_id,
                              capacity=capacity,
                              description=description,
                              faculty=faculty)
        classroom.save()
        return classroom


class EnrrollmentManager(BaseUserManager):
    def create_enrrollment(self, student, course):
        enrrollment = Enrrollment(student=student,
                                  course=course)
        enrrollment.save()
        return enrrollment


class CourseManager(BaseUserManager):
    def create_course(self, quota, priority, from_date_vote, until_date_vote, semester, course, professor):
        course = CourseDetail(quota=quota,
                              priority=priority,
                              from_date_vote=from_date_vote,
                              until_date_vote=until_date_vote,
                              semester=semester,
                              course=course,
                              professor=professor)
        course.save()
        return course


class CourseScheduleManager(BaseUserManager):
    def create_schedule(self, avaliable, course):
        course = CourseSchedule(avaliable=avaliable,
                                course=course)
        course.save()
        return course


class StudentVoteManager(BaseUserManager):
    def create_studentvote(self, student, schedule):
        vote = StudentVote(student=student, schedule=schedule)
        vote.save()
        return vote
    
class ProfessorVoteManager(BaseUserManager):
    def create_professorvote(self, professor, schedule):
        vote = ProfessorVote(professor=professor, schedule=schedule)
        vote.save()
        return vote

# Models


class Secretary(User):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Secretary'
        verbose_name_plural = 'Secreataries'


class Professor(User):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = ProfessorManager()

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professors'


class Student(User):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    objects = StudentManager()

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Faculty(models.Model):
    name = models.CharField(max_length=64)
    date_reg = models.DateTimeField(auto_now=True)
    date_mod = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=True)

    def __str__(self):
        return '{} | {}'.format(self.id, self.name)


class Program(models.Model):
    program_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32)
    date_reg = models.DateTimeField(auto_now=True)
    date_mod = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)


class Course(models.Model):
    course_id = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=1024, default="", blank=True)
    date_reg = models.DateTimeField(auto_now=True)
    date_mod = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return '{}. {}'.format(self.id, self.name)


class Semester(models.Model):
    year = models.IntegerField(default=0)
    period = models.IntegerField(default=0)
    from_date = models.DateField(default=datetime.now)
    until_date = models.DateField(default=datetime.now)
    date_reg = models.DateTimeField(auto_now=True)
    date_mod = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=True)

    objects = SemesterManager()

    class Meta:
        unique_together = ('year', 'period')

    def __str__(self):
        return '{} | {}-{}'.format(self.id, self.year, self.period)


class CourseDetail(models.Model):
    quota = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    from_date_vote = models.DateTimeField(default=datetime.now)
    until_date_vote = models.DateTimeField(default=datetime.now)
    date_reg = models.DateTimeField(auto_now=True)
    date_mod = models.DateTimeField(auto_now=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    objects = CourseManager()

    class Meta:
        unique_together = ('semester', 'course')

    def __str__(self):
        return '{}-{}'.format(self.course, self.professor)


class Enrrollment(models.Model):
    date_reg = models.DateTimeField(auto_now=True)
    date_mod = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)

    objects = EnrrollmentManager()

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return '{}. {}'.format(self.course, self.student)


class Classroom(models.Model):
    classroom_id = models.CharField(max_length=8)
    capacity = models.IntegerField(default=0)
    description = models.CharField(max_length=1024, default="", blank=True)
    date_reg = models.DateTimeField(auto_now=True)
    date_mod = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    objects = ClassroomManager()

    class Meta:
        unique_together = ('classroom_id', 'faculty')

    def __str__(self):
        return '{} {}'.format(self.id, self.faculty)


class Schedule(models.Model):
    time_from = models.TimeField()
    time_to = models.TimeField()
    day = models.CharField(max_length=16)
    date_reg = models.DateTimeField(auto_now=True)
    date_mod = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=True)

    objects = ScheduleManager()

    class Meta:
        unique_together = ('time_from', 'time_to', 'day')

    def __str__(self):
        return '{} - {} | {}'.format(self.time_from, self.time_to, self.day)


class AvaliableHour(models.Model):
    date_reg = models.DateTimeField(auto_now=True)
    date_mod = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    objects = AvaliableHourManager()

    class Meta:
        unique_together = ('schedule', 'classroom')

    def __str__(self):
        return '{} || {}'.format(self.classroom, self.schedule)


class CourseSchedule(models.Model):
    date_reg = models.DateTimeField(auto_now=True)
    date_mod = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=True)
    avaliable = models.ForeignKey(AvaliableHour, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)

    objects = CourseScheduleManager()

    class Meta:
        unique_together = ('avaliable', 'course')

    def __str__(self):
        return '{} || {}'.format(self.avaliable, self.course)


class StudentVote(models.Model):
    date_reg = models.DateTimeField(auto_now=True)
    date_mod = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE)

    objects = StudentVoteManager()

    class Meta:
        unique_together = ('student', 'schedule')


class ProfessorVote(models.Model):
    date_reg = models.DateTimeField(auto_now=True)
    date_mod = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE)
    
    objects = ProfessorVoteManager()

    class Meta:
        unique_together = ('professor', 'schedule')
