# -*- coding: utf-8 -*-

from django.db import models
from students.models.groups import Group
class Student(models.Model):
    """Student Model"""

    class Meta(object):
        verbose_name = "Студент"
        verbose_name_plural = "Студенти"


    first_name = models.CharField(
        max_length = 256,
        blank = False,
        verbose_name = "Ім'я")

    last_name = models.CharField(
        max_length = 256,
        blank = False,
        verbose_name = "Прізвище")

    middle_name = models.CharField(
        max_length = 256,
        blank = True,
        verbose_name = "По-батькові",
        default = '')

    student_group = models.ForeignKey('Group',
        verbose_name=u"Група",
        blank=False,
        null=True,
        on_delete=models.PROTECT)

    birthday = models.DateField(
        blank = True,
        verbose_name = "Дата народження",
        null = True)

    photo = models.ImageField(
        blank = True,
        verbose_name = "Фото",
        null = True)

    ticket = models.CharField(
        max_length = 256,
        blank = False,
        verbose_name = "Білет")

    notes = models.TextField(
        blank = True,
        verbose_name = "Додаткові нотатки")

    lectures = models.ManyToManyField('Lecture', db_table=u'students_lecture_present_students',
       verbose_name=u'Відвідувані заннятя')


    def  __str__(self):
        group = Group.objects.get(student=self)
        return "%s %s  (Група %s)" % (self.first_name, self.last_name, group.title)


