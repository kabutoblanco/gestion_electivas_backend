from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class User(AbstractUser):
    user_id = models.IntegerField(default=0, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(_('email address'), unique=True)    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.username)


#Manager models
class ProfessorManager(BaseUserManager):    
    def create_professor(self, first_name, last_name, email, password):
        if email is None:
            raise TypeError('Users must have an email address.')
        username = email.split('@')[0]
        proffesor = Professor(username=username, first_name=first_name, last_name=last_name, 
                            email=self.normalize_email(email),)
        proffesor.set_password(password)
        proffesor.save()
        return proffesor
    
class StudentManager(BaseUserManager):
    def create_student(self, first_name, last_name, email, password):
        if email is None:
            raise TypeError('Users must have an email address.')
        username = email.split('@')[0]
        student = Student(username=username, first_name=first_name, last_name=last_name, 
                            email=self.normalize_email(email),)
        student.set_password(password)
        student.save()
        return student
    
class SemesterManager(BaseUserManager):
    def create_semester(self, year, period, from_date, until_date, from_date_vote, until_date_vote):
        semester = Semester(year=year,
                            period=period,
                            from_date=from_date,
                            until_date=until_date,
                            from_date_vote=from_date_vote, 
                            until_date_vote=until_date_vote)
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
        

#Models
class Secretary(User):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Secretary'
        verbose_name_plural = 'Secreataries'
    
class Professor(User):  
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    objects = ProfessorManager()
    
    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professors'
    
class Student(User):  
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    objects = StudentManager()
    
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        
class Faculty(models.Model):
    name = models.CharField(max_length=64)
    date_reg = models.DateTimeField(default=timezone.now())
    date_mod = models.DateTimeField(default=timezone.now())
    state = models.BooleanField(default=True)
    
    def __str__(self):
        return '{}'.format(self.name)
        
class Program(models.Model):
    program_id = models.CharField(max_length=32, unique=True)  
    name = models.CharField(max_length=32)   
    date_reg = models.DateTimeField(default=timezone.now())
    date_mod = models.DateTimeField(default=timezone.now())
    state = models.BooleanField(default=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}'.format(self.name)
    
class Course(models.Model):
    course_id = models.CharField(max_length=32)  
    name = models.CharField(max_length=32)    
    description = models.CharField(max_length=64)
    date_reg = models.DateTimeField(default=timezone.now())
    date_mod = models.DateTimeField(default=timezone.now())
    state = models.BooleanField(default=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}. {}'.format(self.id, self.name)
        
class Semester(models.Model):
    year = models.IntegerField(default=0)
    period = models.IntegerField(default=0)
    from_date = models.DateField(default=timezone.now)
    until_date = models.DateField(default=timezone.now)
    from_date_vote = models.DateTimeField(default=timezone.now)
    until_date_vote = models.DateTimeField(default=timezone.now)
    date_reg = models.DateTimeField(default=timezone.now())
    date_mod = models.DateTimeField(default=timezone.now())
    state = models.BooleanField(default=True)
    
    objects = SemesterManager()
    
    class Meta:
        unique_together = ('year', 'period')
    
    def __str__(self):
        return '{}-{}'.format(self.year, self.period)

class CourseDetail(models.Model):
    quota = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    date_reg = models.DateTimeField(default=timezone.now())
    date_mod = models.DateTimeField(default=timezone.now())
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE) 
    proffesor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('semester', 'course')
    
class Enrrollment(models.Model):
    date_reg = models.DateTimeField(default=timezone.now())
    date_mod = models.DateTimeField(default=timezone.now())
    state = models.BooleanField(default=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)
    
class Classroom(models.Model):
    classroom_id = models.CharField(max_length=8)
    capacity = models.IntegerField(default=0)
    description = models.CharField(max_length=64)
    date_reg = models.DateTimeField(default=timezone.now())
    date_mod = models.DateTimeField(default=timezone.now())
    state = models.BooleanField(default=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    
    objects = ClassroomManager()
    
    def __str__(self):
        return '{}'.format(self.classroom_id)

class Schedule(models.Model):
    time_from = models.TimeField(default=timezone.now())
    time_to = models.TimeField(default=timezone.now())
    day = models.CharField(max_length=16)
    date_reg = models.DateTimeField(default=timezone.now())
    date_mod = models.DateTimeField(default=timezone.now())
    state = models.BooleanField(default=True)
    
    objects = ScheduleManager()
    
    class Meta:
        unique_together = ('time_from', 'time_to', 'day')
        
    def __str__(self):
        return '{} - {} | {}'.format(self.time_from, self.time_to, self.day)

class AvaliableHour(models.Model):
    date_reg = models.DateTimeField(default=timezone.now())
    date_mod = models.DateTimeField(default=timezone.now())
    state = models.BooleanField(default=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    
    objects = AvaliableHourManager()
    
    def __str__(self):
        return '{} || {}'.format(self.classroom, self.schedule)
    
    class Meta:
        unique_together = ('schedule', 'classroom')
    
class CourseSchedule(models.Model):
    date_reg = models.DateTimeField(default=timezone.now())
    date_mod = models.DateTimeField(default=timezone.now())
    state = models.BooleanField(default=True)
    avaliable = models.ForeignKey(AvaliableHour, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)
    
class StudentVote(models.Model):
    date_reg = models.DateTimeField(default=timezone.now())
    date_mod = models.DateTimeField(default=timezone.now())
    state = models.BooleanField(default=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE)    
    
    class Meta:
        unique_together = ('student', 'schedule')

