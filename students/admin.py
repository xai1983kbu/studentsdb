from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
from django import forms

from students.models.students import Student
from students.models.groups import Group
from students.models.lectures import Lecture
from students.models.subjects import Subject
from students.models.schoolyears import SchoolYear
from students.models.exams import Exam
from students.models.teachers import Teacher


class StudentFormAdmin(ModelForm):
    def clean_student_group(self):
        '''Check if student is leader in any group.
        If yes, then ensure it’s the same as selected group.'''
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and \
            self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError('Студент є старостою іншої групи.', code='invalid')

        return self.cleaned_data['student_group']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
    form = StudentFormAdmin

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs = {'pk': obj.id})


class GroupFormAdmin(ModelForm):
    def clean(self):
        '''Даний валідатор не дозволить обрати студента, якщо він
           не належить до поточної групи 
           (тобто його поле student_group не вказує на дану групу).'''
        super().clean()
        leader =  self.cleaned_data.get('leader')
        title = self.cleaned_data.get('title')
        group = Group.objects.filter(title = title)
        #import pdb; pdb.set_trace()
        if leader is not None and leader.student_group not in group:
            raise ValidationError(
                      ('Цей студент не з цієї групи! '
                      'Обрати можна тільки студента з групи %(value)s'),
                      params={'value': title},
                  )


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader', 'notes']
    list_display_links = ['title', 'notes']
    list_editable = ['leader']
    ordering = ['leader']
    list_filter = ['title', 'leader']
    list_per_page = 10
    search_fields = ['leader__first_name', 'leader__last_name']
    form = GroupFormAdmin

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs = {'pk': obj.id})

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Lecture)
admin.site.register(Subject)
admin.site.register(SchoolYear)
admin.site.register(Exam)
admin.site.register(Teacher)
