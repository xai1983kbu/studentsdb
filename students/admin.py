from django.contrib import admin
from students.models.students import Student
from students.models.groups import Group
from students.models.lectures import Lecture
from students.models.subjects import Subject
from students.models.schoolyears import SchoolYear

# Register your models here.
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Lecture)
admin.site.register(Subject)
admin.site.register(SchoolYear)
