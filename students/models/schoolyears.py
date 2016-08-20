# -*- coding: utf-8 -*-

from django.db import models

class SchoolYear(models.Model):
    """SchoolYear Model"""

    class Meta(object):
        verbose_name = "Навчальний рік"
        verbose_name_plural = "Навчальні роки"

    title = models.CharField(
        verbose_name=u"Назва навчального року",
        max_length=100,
        blank=False)

    start_year_date = models.DateField(
        verbose_name = "Дата початку навчального року",
        blank=False)

    end_year_date = models.DateField(
        verbose_name = "Дата завершення навчального року",
        blank=False)

    notes = models.TextField(
        blank = True,
        verbose_name = "Додаткові нотатки")


    def __str__(self):
        return "%s (%s : %s)" % (self.title, self.start_year_date, self.end_year_date)
