from django.contrib import admin
from .models import CustomUser, Admin, School, Teacher, Student, Subject, Mark, SubjectStudent

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Admin)
admin.site.register(School)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Mark)
admin.site.register(SubjectStudent)
