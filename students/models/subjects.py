# -*- coding: utf-8 -*-

from django.db import models

class Subject(models.Model):
    """DateLecture Model"""

    class Meta(object):
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"

    title = models.CharField(
        max_length = 256,
        blank = True,
        verbose_name = "Назва предмету")

    date = models.DateField(
        blank = True,
        verbose_name = "Дата проведення екзамену",
        null = True)

    notes = models.TextField(
        blank = True,
        verbose_name = "Додаткові нотатки")
 

    def __str__(self):
        return "%s" % (self.title)
