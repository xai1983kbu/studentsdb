# -*- coding: utf-8 -*-

from django.db import models

class MonthDays(models.Model):
    # list of days, each says whether student was presenеt or not
    for day in range(1,32):
        #http://www.diveintopython.net/html_processing/locals_and_globals.html
        locals()['present_day'+str(day)] = models.BooleanField(default=False)

    #http://stackoverflow.com/questions/16655097/django-abstract-models-versus-regular-inheritance
    class Meta:
        abstract = True


class MonthJournal(MonthDays):
    """Student Monthly Journal"""

    class Meta:
        verbose_name = "Місячний Журнал"
        verbose_name_plural = "Місячні Журнали"

    student = models.ForeignKey('Student',
                  verbose_name="Студент",
                  blank=False,
                  unique_for_month='date')

    # we only need year and month, so always set day to first day of the month
    date = models.DateField(
               verbose_name="Дата",
               blank=False) 

    def  __str__(self):
        return "%s: %d, %d" % (self.student.last_name, \
            self.date.month, self.date.year)




#f = models.BooleanField(default=False)
#for day in range(1,32):
#    setattr(MonthJournal,''.join(('present_day', str(day))), f)

