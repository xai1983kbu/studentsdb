# -*- coding: utf-8 -*-

from django.db import models
from students.models.students import Student
from students.models.groups import Group
from students.models.schoolyears import SchoolYear
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models import Q

class Lecture(models.Model):
    """Lecture Model"""

    class Meta(object):
        verbose_name = "Перелік занять"
        verbose_name_plural = "Перелік занять"

    title = models.ForeignKey('Subject',
        verbose_name=u"Назва предмету(лекції)",
        blank=False,
        null=True,
        on_delete=models.PROTECT)
   
    year = models.ForeignKey('SchoolYear',
        verbose_name=u"Назва навчального року",
        blank=False,
        on_delete=models.PROTECT)
 
    date = models.DateField(
        blank = False,
        verbose_name = "Дата проведення уроку з вибраного предмету")

    title = models.ForeignKey('Subject',
        verbose_name=u"Назва предмету(лекції)",
        blank=False,
        on_delete=models.PROTECT)
    
    group = models.ForeignKey('Group',
        verbose_name=u"Назва групи для якої проводиться заняття",
        blank=False,
        on_delete=models.PROTECT)
 
    present_students = models.ManyToManyField('Student', db_table=u'students_lecture_present_students',
        verbose_name=u'Відвідувачі заняття',
        blank=True)

    notes = models.TextField(
        blank = True,
        verbose_name = "Додаткові нотатки")


    def __str__(self):
        students = Student.objects.filter(lecture=self)
        return "%s (%s)(%s)" % (self.title, self.date, students)
    

    def clean(self, *args, **kwargs):
        start = self.year.start_year_date
        end = self.year.end_year_date
        if self.date < start or self.date > end:
            raise ValidationError({'date': ('Дата виходить за межі вказаного навчального року')})

        super(Lecture, self).clean(*args, **kwargs)


    def save(self, *args, **kwargs):
        self.full_clean()
        super(Lecture, self).save(*args, **kwargs)





