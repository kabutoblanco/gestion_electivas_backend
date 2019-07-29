from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import *

# Register your models here.

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
            'fields': ('user_id', 'email', 'password1', 'password2', 'username'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(Secretary, UserAdmin)
admin.site.register(Professor, UserAdmin)
admin.site.register(Student, UserAdmin)
admin.site.register(Semester)
admin.site.register(Schedule)
admin.site.register(Classroom)
admin.site.register(Faculty)
admin.site.register(Program)
admin.site.register(AvaliableHour)
admin.site.register(Course)
admin.site.register(CourseDetail)
admin.site.register(Enrrollment)
admin.site.register(CourseSchedule)