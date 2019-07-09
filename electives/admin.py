from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User, Secretary, Professor, Student, Course, Semester, Schedule, Classroom, Faculty, AvaliableHour, Program

# Register your models here.
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Semester)
admin.site.register(Schedule)
admin.site.register(Classroom)
admin.site.register(Faculty)
admin.site.register(Program)
admin.site.register(AvaliableHour)
admin.site.register(Course)

class UserProfileInline(admin.StackedInline):
    model = Secretary
    can_delete = False

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    inlines = (UserProfileInline, )